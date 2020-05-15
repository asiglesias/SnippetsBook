
from webapp2_extras import jinja2
import hashlib
from models.user import User
from handlers.base import BaseHandler
from models.snippet import Snippet
from google.appengine.ext import ndb
import time
from models.usersnippet import Rate



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
        time.sleep(0.5)

        self.redirect("/mysnippets")


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


class EditSnippetHandler(BaseHandler):
    def get(self):
        if not self.is_logged_user():
            self.redirect('/login')
            return

        id = self.request.get("id", None)

        if  id is None:
            return self.redirect('/mysnippets')

        snippet = ndb.Key(urlsafe=id).get()
        user_snippet = snippet.user.get()
        if not user_snippet.username == self.session.get("user"):
            return self.redirect('/mysnippets')

        data = {
            'snippet': snippet,
            'is_logged': self.is_logged_user()
        }

        jinja = jinja2.get_jinja2(app=self.app)
        return self.response.write(jinja.render_template('snippets/edit_snippet.html', **data))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)

        if not self.is_logged_user():
            self.redirect("/login")
            return

        id = self.request.get("id", None)

        if id is None:
            return self.redirect('/mysnippets')

        snippet = ndb.Key(urlsafe=id).get()


        title = self.request.get("title", None)
        description = self.request.get("description", None)
        code = self.request.get("code", None)



        if title is None or description is None or code is None:
            self.redirect("/newsnippet")
            return


        snippet.name = title
        snippet.description = description
        snippet.code = code
        k = snippet.put()
        time.sleep(0.5)
        self.redirect("/mysnippets")

class RateSnippetHandler(BaseHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        if not self.is_logged_user():
            self.redirect("/login")
            return

        id = self.request.get("id", None)
        valoration_positive = False if self.request.get("positive", 'False') == 'False' else True

        if id is None:
            return self.redirect('/mysnippets')

        snippet = ndb.Key(urlsafe=id).get()

        user = User.query(User.username == self.session.get('user')).get()
        rate = Rate.query(Rate.user == user.key, Rate.snippet == snippet.key).get()
        if rate:
            if valoration_positive == rate.positive_valoration:
                return self.redirect('/')
            else:
                rate.positive_valoration = valoration_positive
                rate.put()
                if valoration_positive:
                    snippet.score += 1
                else:
                    snippet.score -= 1
                snippet.put()
                time.sleep(0.5)
                return self.redirect('/')


        rate = Rate(user=user.key, snippet=snippet.key, positive_valoration=valoration_positive)

        if valoration_positive:
            snippet.score += 1
        else:
            snippet.score -= 1

        rate.put()
        snippet.put()
        time.sleep(0.5)
        return self.redirect('/')














