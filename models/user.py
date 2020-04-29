
from google.appengine.ext import ndb


class Snippet(ndb.Model):
    username = ndb.IntegerProperty(required=True)
    email = TextProperty(required=True)
    password = ndb.IntegerProperty(required=True)