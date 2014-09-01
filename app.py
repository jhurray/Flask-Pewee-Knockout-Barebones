import sys
import json
from flask import Flask
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for, abort, render_template, flash
# my classes
from web_cache import *
# uncomment if you want to use a database
from database import *

# config - aside from our database, the rest is for use by Flask
DEBUG = True
DATABASE = False

# create a flask application - this ``app`` object will be used to handle
# inbound requests, routing them to the proper 'view' functions, etc
app = Flask(__name__)
app.config.from_object(__name__)

# request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.  peewee will do
# this for us, but its generally a good idea to be explicit.
@app.before_request
def before_request():
    g.db = db if DATABASE else None
    if g.db:
      g.db.connect()

@app.after_request
def after_request(response):
    if g.db:
      g.db.close()
    return response

@app.route('/')
def home():
  return render_template('home.html', message="My flask peewee template app!!!")


@app.route('/myendpoint', methods=['GET', 'POST'])
def getexample():

  if request.method is 'POST':
    # do stuff
    responseObj = dict(message="this was from a post request!")
  elif request.method is 'GET':
    # do other stuff
    responseObj = dict(message="this was from a get request!")
  # json response
  return json.dumps(responseObj)


# allow running from the command line
if __name__ == '__main__':
  app.run()


