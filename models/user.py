
from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    email = ndb.TextProperty(required=True)
    password = ndb.StringProperty(required=True)