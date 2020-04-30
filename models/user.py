
from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.IntegerProperty(required=True)
    email = ndb.TextProperty(required=True)
    password = ndb.IntegerProperty(required=True)