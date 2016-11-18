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
This facilitates the upload process, but is also good practice with any codebase.

~~~
vim .gitignore
git init
git add -A
git commit -m "initial commit"
~~~



## Testing Locally

## Uploading to Heroku
