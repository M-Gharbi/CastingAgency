import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate



#database_path ='postgres://xxxx'


database_name = "casting_test"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'Mm@0559372667','localhost:5432', database_name)

#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    #db.drop_all()
    db.create_all()
    dummyData()

 



def dummyData():
    movie1 = Movie(title="Movie 1", release_date="1/1/2020")
    movie2 = Movie(title="Movie 2", release_date="1/1/2020")
    movie3 = Movie(title="Movie 3", release_date="1/1/2020")
    actor1 = Actor(name="First", age=18, gender="male")
    actor2 = Actor(name="Second", age=25, gender="female")
    actor3 = Actor(name="Gharbi", age=40, gender="male")
    actor4 = Actor(name="Mary", age=13, gender="female")
    actor5 = Actor(name="Nora", age=16, gender="femal")
    actor6 = Actor(name="Mohammed", age=20, gender="male")

    Movie.insert(movie1)
    Movie.insert(movie2)
    Movie.insert(movie3)
    Movie.insert(actor1)
    Actor.insert(actor2)
    Actor.insert(actor3)
    Actor.insert(actor4)
    Actor.insert(actor5)
    Actor.insert(actor6)

    association1 = association.insert().values(
        movie_id=movie1.id, actor_id=actor1.id)
    association2 = association.insert().values(
        movie_id=movie1.id, actor_id=actor2.id)
    association3 = association.insert().values(
        movie_id=movie1.id, actor_id=actor3.id)
    association4 = association.insert().values(
        movie_id=movie1.id, actor_id=actor4.id)
    association5 = association.insert().values(
        movie_id=movie1.id, actor_id=actor5.id)
    association6 = association.insert().values(
        movie_id=movie1.id, actor_id=actor6.id)

    association7 = association.insert().values(
        movie_id=movie2.id, actor_id=actor1.id)
    association8 = association.insert().values(
        movie_id=movie2.id, actor_id=actor2.id)
    association9 = association.insert().values(
        movie_id=movie2.id, actor_id=actor3.id)

    association10 = association.insert().values(
        movie_id=movie3.id, actor_id=actor4.id)
    association11 = association.insert().values(
        movie_id=movie3.id, actor_id=actor5.id)
    association12 = association.insert().values(
        movie_id=movie3.id, actor_id=actor6.id)

    db.session.execute(association1)
    db.session.execute(association2)
    db.session.execute(association3)
    db.session.execute(association4)
    db.session.execute(association5)
    db.session.execute(association6)
    db.session.execute(association7)
    db.session.execute(association8)
    db.session.execute(association9)
    db.session.execute(association10)
    db.session.execute(association11)
    db.session.execute(association12)
    db.session.commit()


association = db.Table('association',
                       Column('movie_id', Integer, db.ForeignKey('Movies.id')),
                       Column('actor_id', Integer, db.ForeignKey('Actors.id')),
                       )    

'''
Movies
 Movies entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):  
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)



    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


'''
Actor
 Actor entity, extends the base SQLAlchemy Model
'''
class Actor(db.Model):  
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        #self.movie = movie

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
