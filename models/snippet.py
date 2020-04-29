
from google.appengine.ext import ndb
from user import User


class Snippet(ndb.Model):
    code = TextProperty(required=True)
    score = ndb.IntegerProperty(default=0)
    user = ndb.KeyProperty(kind=User)
    creation_date = ndb.DateTimeProperty(auto_now_add=True)

