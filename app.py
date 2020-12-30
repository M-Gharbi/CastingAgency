import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask import Flask, request, render_template
from models import setup_db, Movie, Actor, db, dummyData
from models import db_drop_and_create_all
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''

    db_drop_and_create_all()


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/callback')
    def callback_handling():
        return render_template('logged-in.html')


    '''
    @TODO implement endpoint
        GET /movies
    '''


    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        try:
            movies = Movie.query.all()
            movies_format = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'Movies': movies_format
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        GET /actors
    '''


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        try:
            actors = Actor.query.all()
            actors_format = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'Actors': actors_format
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        GET /movies/<int:id>
    '''


    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def show_movie(id):
        try:
            movie = Movie.query.filter_by(id=id).first()
            if not movie:
                return abort(404)
            return jsonify({
                'success': True,
                'data': movie.format()
            }), 200
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        GET /actors/<int:id>
    '''


    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def show_actor(id):
        try:
            actor = Actor.query.filter_by(id=id).first()
            if not actor:
                return abort(404)
            return jsonify({
                'success': True,
                'data': actor.format()
            }), 200
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        POST /actors
    '''


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor():
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        if ((name is None) or (age is None) or (gender is None)):
            return abort(400)
        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            Actor.insert(new_actor)
            return jsonify({
                'success': True,
                'actor': new_actor.format()
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        POST /movies
    '''


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie():
        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get("release_date", None)

        if ((title is None) or (release_date is None)):
            return abort(422)
        try:
            new_movie = Movie(title=title, release_date=release_date)
            Movie.insert(new_movie)
            return jsonify({
                'success': True,
                'movie': new_movie.format()
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        PATCH /movies/<id>
            where <id> is the existing model id
    '''


    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(id):
        the_movie = Movie.query.filter(Movie.id == id).one_or_none()
        if the_movie is None:
            return abort(404)

        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get("release_date", None)

        if ((title is None) and (release_date is None)):
            return abort(422)
        try:
            if title is not None:
                the_movie.title = title
            if release_date is not None:
                the_movie.release_date = release_date

            Movie.update(the_movie)
            return jsonify({
                'success': True,
                'actor': the_movie.format()
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        PATCH /actors/<id>
        where <id> is the existing model id
    '''


    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(id):
        the_actor = Actor.query.filter(Actor.id == id).one_or_none()
        if the_actor is None:
            return abort(404)

        data = request.get_json()
        name = data.get('name', None)
        age = data.get("age", None)
        gender = data.get("gender", None)

        if ((name is None) and (age is None) and (gender is None)):
            return abort(422)
        try:
            if name is not None:
                the_actor.name = name
            if age is not None:
                the_actor.age = age
            if gender is not None:
                the_actor.gender = gender

            Helpers.update(the_actor)
            return jsonify({
                'success': True,
                'actor': the_actor.format()
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        DELETE /movies/<id>
            where <id> is the existing model id
    '''


    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(id):
        try:
            movie = Movie.query.filter_by(id=id).first()
            if not movie:
                return abort(404)

            Movie.delete(movie)
            return jsonify({
                'success': True,
                'deleted': movie.id,
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    '''
    @TODO implement endpoint
        DELETE /actors/<id>
            where <id> is the existing model id
    '''


    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(id):
        try:
            actor = Actor.query.filter_by(id=id).first()
            if not actor:
                return abort(404)
            Actor.delete(actor)
            return jsonify({
                'success': True,
                'deleted': actor.id,
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    '''
    Error Handling
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422


    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code


    return app



app = create_app()

if __name__ == '__main__':
    app.run()