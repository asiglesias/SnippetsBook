
from google.appengine.ext import ndb
from user import User


class Snippet(ndb.Model):
    code = TextProperty(required=True)
    score = ndb.IntegerProperty()
    user = ndb.KeyProperty(kind=User)

