
from webapp2_extras import jinja2
import hashlib
from models.user import User
from handlers.base import BaseHandler
from models.snippet import Snippet
from google.appengine.ext import ndb
import time



class CreateSnippetHandler(BaseHandler):
    def get(self):

        data = {
            "is_logged": self.is_logged_user()
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("snippets/create_snippet.html", **data))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)

        if not self.is_logged_user():
            self.redirect("/login")
            return

        title = self.request.get("title", None)
        description = self.request.get("description", None)
        code = self.request.get("code", None)

        if title is None or description is None or code is None:
            self.redirect("/newsnippet")
            return

        username = self.session['user']
        user = User.query(User.username == username).get()

        snippet = Snippet(code=code, name=title, description=description, user=user.key)
        k = snippet.put()

        self.redirect("/")


class MySnippetsHandler(BaseHandler):

    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        if not self.is_logged_user():
            self.redirect('/login')
            return

        user = User.query(User.username == self.session['user']).get()
        snippets = Snippet.query(Snippet.user == user.key).fetch()

        for snippet in snippets:
            user = User.query(User.key == snippet.user).get()
            snippet.completeuser = user

        data = {
            "is_logged": self.is_logged_user(),
            "snippets": snippets
        }

        self.response.write(jinja.render_template("mysnippets/mysnippets.html", **data))

class DeleteSnippetHandler(BaseHandler):
    def get(self):

        if not self.is_logged_user():
            self.redirect('/login')
            return

        id = self.request.get("id", None)
        if not id is None:
            snippet = ndb.Key(urlsafe=id).get()
            snippet.key.delete()
            time.sleep(0.5)
            return self.redirect("/mysnippets")










