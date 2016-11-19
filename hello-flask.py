import os
import urlparse
import psycopg2

from flask import Flask, g

app = Flask(__name__)

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

@app.route('/')
def index():
  return 'Hello, Flask!'

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

if __name__ == '__main__':
  app.run()
