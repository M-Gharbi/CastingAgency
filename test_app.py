import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

assistant_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InltaUc1WHNpYkx1akFXTnVVWFdNVCJ9.eyJpc3MiOiJodHRwczovL2Fsc2hhbW1hcmkudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTc1NDIyMDgyODRiMDA2YmI1MmJkMyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDkxNjU3MTQsImV4cCI6MTYwOTE3MjkxNCwiYXpwIjoiTXJpU2UxdldWaDgxenpub0NSVmtNa0F1TmUwUGo3eDciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.VKu9UMFXUuYqZI5bJhc9ti8ncSx-JqtEz_dymKbC9Rf9WJTyaAcs4D6WlngJ5HRFZ4wyRA6SOYVaM6XMzBHyM9aqbOBhsWApxBcTEpAo4kJ32jS6Nluc2Rdseerlw71D0pmSonQ2xScFhAtugbp-dgs9RtoTEWKHDPI07YrCOanoQKF95JD3Zw6pTypKVdAX80klohBzK5Lt54_QYkRjaEjAOzxVn9U-KEheqgb_1SiMI6LNr-UkA2VocDh1ygmsGgGHW5kOOoWPxu3ja_hKd_aJwaZIfQUjSTwq2EBpPMIphlMD7JBK92qRJETx8shaB6QspA_t5KfFXce-J10luA"
}

director_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InltaUc1WHNpYkx1akFXTnVVWFdNVCJ9.eyJpc3MiOiJodHRwczovL2Fsc2hhbW1hcmkudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTc1NGIwNTY5NmFlMDA3MTJlNjNkZSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDkxNjU4MzUsImV4cCI6MTYwOTE3MzAzNSwiYXpwIjoiTXJpU2UxdldWaDgxenpub0NSVmtNa0F1TmUwUGo3eDciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.p29X8Pv1CbVVXfDCtRXdktlbMTFHYDcxvN6gSOkQA0cwNbJmCQwt0BcYfovNLucZfqVnnkA2r0kygxhJmEgd4kcE_DM6QRPHPU2I2wpxAMv9qOTAd4Y_A-SHpe84jgilS0WUlrIhTrm1_OtskvJaBWRZurcRfeFlw2cl1NEGjK9M1Vn1lvUXHVOMB49eykmOTHIWm0pT--pWsjPychCnzW8-f5w2g8Ohn_5H1-WpmJNoSRJNgDaRz7kxopzjyjkusgkPPZ3N3BtdgJdKUBKo0c13RwAuduFZO8Zs_fhXEvwdOV05hszo-RQ52K7CmRFefiL93QYmqww45vbvHTSn8A"
}

producer_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InltaUc1WHNpYkx1akFXTnVVWFdNVCJ9.eyJpc3MiOiJodHRwczovL2Fsc2hhbW1hcmkudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTc1NTIzODE2MzdiMDA2ODVjY2YwNiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDkxNjU5NDYsImV4cCI6MTYwOTE3MzE0NiwiYXpwIjoiTXJpU2UxdldWaDgxenpub0NSVmtNa0F1TmUwUGo3eDciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jx8gSv70y5fjewYDXA0LyMmpnEHPNPDo1XwzSucWcaqMx_ov3hEpP7cJ16e3qjjkxa4X5KLmwmClBH6ilcTxkWje5LFmXXkdVoCs0_k_7tLk9iguqYTx2_sWfeGRHrksyA-2jW0rSIswcNrCMRoxjonO0VodQakCS9e_9Dh9YHneHF9mPtAtuH-fVi1mdUU58cg4i19CwivFQCpQNHU-HED02rXgWsrn7-Hzqx-w0kVbWpRHDGRh-GYUJk0fd9VQy36AEFBqTRKWOlWw4tjuVnM5JuxCE-qCpTrFub40wJBf0QU5DSTTWHOEHCm8x16n0Z1YM_lwGFgqXWgssWQU_w"
}


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "casting_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'Mm@0559372667','localhost:5432', 'casting_test')

        setup_db(self.app, self.database_path)
        self.new_actor = {
            'name': 'test name',
            'age': 99,
            'gender': 'male'
        }
        self.new_movie = {
            'title': 'test Movie',
            'release_date': '10/10/2044'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Success
    # Actors Endpoints
    def test_get_actors(self):
        """Test getting actors"""
        response = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Actors'])
        self.assertTrue(len(data['Actors']))

    def test_get_actor_by_id(self):
        """Test get actor by id"""
        response = self.client().get('/actors/{}'.format(1), headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_delete_actor(self):
        """Test delete actor"""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Actor.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def test_create_actors(self):
        """Test create actor"""

        actors_before = Actor.query.all()
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=producer_auth_header)
        data = json.loads(response.data)
        actors_after = Actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(actors_after) == len(actors_before) + 1)

        # delete the actor to insure db consistency
        created_actor = Actor.query.order_by(Actor.id.desc()).first()
        Actor.delete(created_actor)

    # Movies Endpoints
    def test_get_movies(self):
        """Test getting movies"""
        response = self.client().get('/movies', headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def test_get_movie_by_id(self):
        """Test get movie by id"""
        response = self.client().get('/movies/{}'.format(1), headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_delete_movie(self):
        """Test delete movie"""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Movie.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def test_create_movies(self):
        """Test create movie"""
        movies_before = Movie.query.all()
        response = self.client().post('/movies', json=self.new_movie,
                                      headers=producer_auth_header)
        data = json.loads(response.data)
        movies_after = Movie.query.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(movies_after) == len(movies_before) + 1)
        # delete the movie to insure db consistency
        created_movie = Movie.query.order_by(Movie.id.desc()).first()
        Movie.delete(created_movie)

    # RBAC Tests
    # all the roles can see the movies

    def get_movies_as_assistant_successfully(self):
        """Test getting movies as assistant."""
        response = self.client().get('/movies', headers=assistant_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def get_movies_as_director_successfully(self):
        """Test getting movies as director."""
        response = self.client().get('/movies', headers=director_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def get_movies_as_producer_successfully(self):
        """Test getting movies as producer."""
        response = self.client().get('/movies', headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    # Only Casting Director and Excutive Producer can delete an actor
    def delete_actor_as_assistant_unsuccessfully(self):
        """Test delete actor as assistant."""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Actor.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=assistant_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], 'false')
        self.assertEqual(data['message'], 'permission key not found')
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_actor_as_director_successfully(self):
        """Test delete actor as director."""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Actor.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=director_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_actor_as_producer_successfully(self):
        """Test delete actor as producer."""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Actor.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    # Only Excutive Producer can delete a movie
    def delete_movie_as_assistant_unsuccessfully(self):
        """Test delete movie as assistant."""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Movie.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=assistant_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], 'false')
        self.assertEqual(data['message'], 'permission key not found')
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_movie_as_director_unsuccessfully(self):
        """Test delete movie as director."""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Movie.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=director_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], 'false')
        self.assertEqual(data['message'], 'permission key not found')
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_movie_as_producer_successfully(self):
        """Test delete movie as producer."""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Movie.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    # Error
    # Actors Endpoints
    def test_404_delete_actor(self):
        """Test delete non-existed actor"""

        response = self.client().delete('/actors/{}'.format(int(9999)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    def test_404_get_actor(self):
        """Test get non-existed actor"""

        response = self.client().get('/actors/{}'.format(int(9999)),
                                     headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_400_create_actor(self):
        """Test create actor with empty data"""

        response = self.client().post('/actors', json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'BAD REQUEST')

    def test_404_update_non_existed_actor(self):
        """Test update non-existed actor"""

        response = self.client().patch('/actors/{}'.format(int(9999)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_422_update_actor(self):
        """Test update actor with empty parmas"""

        response = self.client().patch('/actors/{}'.format(int(1)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    # Movies Endpoints
    def test_404_delete_movie(self):
        """Test delete non-existed movie"""

        response = self.client().delete('/movies/{}'.format(int(9999)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    def test_404_get_movie(self):
        """Test get non-existed movie"""

        response = self.client().get('/movies/{}'.format(int(9999)),
                                     headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_422_create_movie(self):
        """Test create movie with empty data"""

        response = self.client().post('/movies', json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    def test_404_update_non_existed_movie(self):
        """Test update non-existed movie"""

        response = self.client().patch('/movies/{}'.format(int(9999)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_422_update_movie(self):
        """Test update movie with empty parmas"""

        response = self.client().patch('/movies/{}'.format(int(1)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
