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
