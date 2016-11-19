# Hello, Flask!

This tutorial demonstrates how to deploy a Flask application on Heroku.

## Writing the App

The app is very simple.
It displays "Hello, Flask!" on the homepage.

`vim hello-flask.py`

~~~
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello, Flask!'

if __name__ == '__main__':
  app.run()
~~~

Assuming Flask is installed, the app can be tested in the browser with `python hello-flask.py`.
Visit `localhost:5000` to see the website.

## Making a Git Repository

In order to deploy to Heroku, the server code should reside in a Git repository.
This facilitates the upload process, and is also good practice with any codebase.

~~~
vim .gitignore
git init
git add -A
git commit -m "initial commit"
~~~

The code can also be added to Github.

~~~
git remote add origin git@github.com:scottmsul/hello-flask.git
git push -u origin master
~~~

## Add Heroku-Specific Files

The `requirements.txt` file is used by `pip` in order to fetch dependencies.
A dependencies file allows Heroku to download the minimum set of Python packages needed to run the app.

`vim requirements.txt`

~~~
flask==0.11.1
gunicorn==19.6.0
~~~

The `Procfile` is used by Heroku to launch the web server.
In particular, the `web: ` prefix says which command launches the server.
The suffix tells gunicorn that the Python file `hello-flask` contains a variable `app` which handles the WSGI interface.

`vim Procfile`

~~~
web: gunicorn hello-flask:app
~~~

Together these files signal Heroku that the back-end is written in Python.

## Testing the Heroku App Locally

To test with the same environment used by Heroku, create a virtual environment.
This will download the package versions in `requirements.txt` and prefer those to any system installs.

~~~
virtualenv venv
source venv/bin/activate
~~~

To run the server locally, use the following command.

`heroku local web`

## Deployment

Log in to Heroku.

~~~
heroku login
~~~

Create a Heroku app if it doesn't already exist.

~~~
heroku create scottmsul-hello-flask
~~~

Commit the current changes (added `requirements.txt` and `Procfile`).

~~~
git add -A
git commit -m "added heroku files"
~~~

Push the changes to Heroku.

~~~
git remote add heroku https://git.heroku.com/scottmsul-hello-flask.git
git push heroku master
~~~

Run the web app.

~~~
heroku ps:scale web=1
~~~

Now were all done! The app can be opened in a browser.

~~~
heroku open
~~~

# Adding a database

Most nontrivial apps require a database.
The following walks through the process of setting up a database on Heroku, and accessing it with Python.

## Install psycopg2

`psycopg2` is the standard Python library for interacting with databases, at least at a low-level (for high-level tools see SQLAlchemy).
To install, add the library to `requirements.txt`.

`vim requirements.txt`
~~~
flask==0.11.1
gunicorn==19.6.0
psycopg2==2.6.1
~~~

## Instantiate a Remote Heroku Database

To instantiate a database, create a postgresql addon.

~~~
heroku addons:create heroku-postgresql:hobby-dev
~~~

The `hobby-dev` tier is free, but only allows for 10k rows.
For other tiers, see [here](https://elements.heroku.com/addons/heroku-postgresql#pricing).

## Add Some Test Rows

The database can be accessed using `heroku pg:pgsql`.
Let's populate the database with a few rows.

`vim schema.sql`

~~~
DROP TABLE IF EXISTS animals;

CREATE TABLE animals (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO animals (name) VALUES ('moose');
INSERT INTO animals (name) VALUES ('bear');
INSERT INTO animals (name) VALUES ('squirrel');
INSERT INTO animals (name) VALUES ('zebra');
~~~

`heroku pg:psql < schema.sql`

## Connect to the Database from Python

The following code connects to the database.

~~~
import os
import urlparse
import psycopg2

def connect():

  urlparse.uses_netloc.append("postgres")
  url = urlparse.urlparse(os.environ["DATABASE_URL"])

  db = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
  )
  return db
~~~

For more information, see [here](https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python).

## Add a View

Once we have access, we can stop worrying about Heroku and focus on Flask-specific code.
The following code adds the database connection to the application context.

~~~
from flask import g

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = connect()
    g._database = db
  return db

def get_cursor():
  return get_db().cursor()

@app.teardown_appcontext
def close_db(error):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()
~~~

The following code sets up a rudimentary view.

~~~
@app.route('/animals')
def animals():
  cursor = get_cursor()
  q = '''
    SELECT name FROM animals;
  '''
  cursor.execute(q)
  animals = cursor.fetchall()
  animals = [animal[0] for animal in animals]
  return str(animals)
~~~

## Add the Database URL to the Local Environment

The previous code should deploy correctly, but let's test it locally.
There was a line of code earlier which was glossed over, mainly `url = urlparse.urlparse(os.environ["DATABASE_URL"])`.
This code assumes the presence of an environment variable named `DATABASE_URL`.
On Heroku, this environment variable will be supplied, but won't be present locally.
To access it locally, create a `.env` file with this variable (this file supplies environment variables when the `heroku local...` command is run).
To determine its correct value, run `heroku config`, which should display the database's url.

`vim .env`

~~~
DATABASE_URL=postgres://{some-stuff}
~~~

It's also a good idea to add `.env` to the `.gitignore` file.

## Test Locally

Try out `heroku local web` and head over to `localhost:5000/animals`.

## Deploy

To deploy, do the usual steps.

~~~
vim .gitignore (add .env)
git add -A
git commit -m "added database"
git push heroku master
~~~

And test it out.

~~~
heroku open
~~~
