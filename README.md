# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This is a system to simplify and streamline the process.

## Tech Used
- Python
- Flask with SQLAlchemy
- Postgres SQL
- Auth0
- Heroku
- Postman

## LIVE URL : https://alshammari-app.herokuapp.com/


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### Set up a Virtual Enviornment
To create a virtual environment, go to your project’s directory and run venv. If you are using Python 2, replace venv with virtualenv in the below commands.

On macOS and Linux:
```bash
python3 -m venv env
```
On Windows:
```bash
py -m venv env
```


#### Activate a Virtual Enviornment
On macOS and Linux:
```bash
source env/bin/activate
```
On Windows:
```bash
.\env\Scripts\activate
```


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to project’s directory running:

pip install -r requirements.txt

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server

From within the directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:


On Linux : export
export FLASK_APP=app.py;
On Windows : set
set FLASK_APP=app.py;

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Setting Up Project Locally
After succesfully installing all requirements for the project. You can setup the project locally by following the steps below:

1. Create Databases. 
```
psql -c "CREATE DATABASE casting" "user=postgres dbname=postgres password=Mm@0559372667"

```

2. Configure the models.py / test_app.py with appropiate variables.
```
database_path ='postgresql://postgres:Mm@0559372667@localhost:5432/casting'

```

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `get:movies`
    - `post:actors`
    - `post:movies`
    - `delete:actors`
    - `delete:movies`
    - `patch:actors`
    - `patch:movies`

6. Create new roles for:
    - Casting Assistant
        - Can view actors and movies

    - Casting Director
        - Can view actors and movies, Add or delete an actor from the database, Modify actors  or movies
    - Executive Producer
        - Can view actors and movies, Add or delete an actor from the database, Modify actors or movies, Add or delete a movie from the database

7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Assistant role, Director role and Executive Producer.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./CAPSTONE/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### API Endpoints Behaviour
Listed below are the Endpoints in the system
- Casting Assistant
  - GET /actors
  - GET /movies
  
- Casting Director
  - GET /actors
  - GET /movies
  - POST /actors
  - PATCH /actors/<int:id>
  - PATCH /movies/<int:id>
  - DELETE /actors/<int:id>
 
- Executive Director
  - GET /actors
  - GET /movies
  - POST /actors
  - POST /movies
  - PATCH /actors/<int:id>
  - PATCH /movies/<int:id>
  - DELETE /actors/<int:id>
  - DELETE /movies/<int:id>


### API Endpoints Behaviour


#### GET /actors
- Return a list of all actors in the Database
- Response: 
```
{"Actors":[{"age":18,"gender":"male","id":1,"name":"First"},{"age":25,"gender":"female","id":2,"name":"Second"},{"age":40,"gender":"male","id":3,"name":"Gharbi"},{"age":13,"gender":"female","id":4,"name":"Mary"},{"age":16,"gender":"femal","id":5,"name":"Nora"},{"age":20,"gender":"male","id":6,"name":"Mohammed"},{"age":18,"gender":"male","id":7,"name":"First"},{"age":25,"gender":"female","id":8,"name":"Second"},{"age":40,"gender":"male","id":9,"name":"Gharbi"},{"age":13,"gender":"female","id":10,"name":"Mary"},{"age":16,"gender":"femal","id":11,"name":"Nora"},{"age":20,"gender":"male","id":12,"name":"Mohammed"},{"age":18,"gender":"male","id":13,"name":"First"},{"age":25,"gender":"female","id":14,"name":"Second"},{"age":40,"gender":"male","id":15,"name":"Gharbi"},{"age":13,"gender":"female","id":16,"name":"Mary"},{"age":16,"gender":"femal","id":17,"name":"Nora"},{"age":20,"gender":"male","id":18,"name":"Mohammed"},{"age":18,"gender":"male","id":19,"name":"First"},{"age":25,"gender":"female","id":20,"name":"Second"},{"age":40,"gender":"male","id":21,"name":"Gharbi"},{"age":13,"gender":"female","id":22,"name":"Mary"},{"age":16,"gender":"femal","id":23,"name":"Nora"},{"age":20,"gender":"male","id":24,"name":"Mohammed"}],"success":true}
```
#### GET /movies
- Return a list of all movies in the Database
- Response:
```
{"Movies":[{"id":1,"release_date":"1/1/2020","title":"Movie 1"},{"id":2,"release_date":"1/1/2020","title":"Movie 2"},{"id":3,"release_date":"1/1/2020","title":"Movie 3"},{"id":4,"release_date":"1/1/2020","title":"Movie 1"},{"id":5,"release_date":"1/1/2020","title":"Movie 2"},{"id":6,"release_date":"1/1/2020","title":"Movie 3"},{"id":7,"release_date":"1/1/2020","title":"Movie 1"},{"id":8,"release_date":"1/1/2020","title":"Movie 2"},{"id":9,"release_date":"1/1/2020","title":"Movie 3"},{"id":10,"release_date":"1/1/2020","title":"Movie 1"},{"id":11,"release_date":"1/1/2020","title":"Movie 2"},{"id":12,"release_date":"1/1/2020","title":"Movie 3"}],"success":true}
```
#### GET /actors/<int:id>
- Return actors by his id
- Response: 
```
{"data":{"age":20,"gender":"male","id":12,"name":"Mohammed"},"success":true}
```
#### GET /movies/<int:id>
- Return a list of all movies in the Database
- Response:
```
{"data":{"id":3,"release_date":"1/1/2020","title":"Movie 3"},"success":true}
```

#### POST /actors
- Create a new Actor, Insert a new actor into the Database
- Request Body : 
```
{
	"name": "name",
	"age": 50,
	"gender": "male"
}
```
- Response:
```
{"actor": {"age": 10,"gender": "male","id": 24,"name": "name"},"success": true}
```

#### POST /movies
- Create a new Movie, Insert a new movie into the Database
- Request Body :
```
{
	"title": "test",
	"release_date": "1/1/2020"
}
```
- Response:
```
{movie": {"actors": [],"id": 13,"release_date": "1/1/2020","title": "test"},"success": true}
```

#### PATCH /movies/<int:id>
- Update an existing Movie details
- Request Body : the title or the release date, Any or Both of these fields can be updated
```
{
	"title": "changed"
}
```
-  Response:
```
{"actor": {"actors": [],"id": 13,"release_date": "1/1/2020","title": "changed"},"success": true}
```

#### PATCH /actors/<int:id>
- Update an existing Actor's Details using the Actor's ID
- Request Body : the Name or the Age or the Gender, any or all of them can be updated
```
{
	"name": "changed"
}
```
- Response:
```
{"actor": {"age": 20,"gender": "male","id": 6,"name": "changed"},"success": true}
```

#### DELETE /actors/<int:id>
- Delete an existing Actor using the Actor's ID
- Example Response:
```
{"deleted": 1,"success": true}
```