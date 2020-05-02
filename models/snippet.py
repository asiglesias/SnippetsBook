
from google.appengine.ext import ndb
from models.user import User


class Snippet(ndb.Model):
    code = ndb.TextProperty(required=True)
    name = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)
    score = ndb.IntegerProperty(default=0)
    user = ndb.KeyProperty(kind=User)
    creation_date = ndb.DateTimeProperty(auto_now_add=True)

