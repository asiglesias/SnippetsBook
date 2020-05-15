
from google.appengine.ext import ndb
from models.user import User
from models.snippet import Snippet


class Rate(ndb.Model):
    user = ndb.KeyProperty(kind=User)
    snippet = ndb.KeyProperty(kind=Snippet)
    positive_valoration = ndb.BooleanProperty(required=True)