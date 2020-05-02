
from webapp2_extras import jinja2
from handlers.base import BaseHandler
import hashlib
from models.user import User


class LogoutHandler(BaseHandler):
    def get(self):
        self.session['user'] = None
        self.redirect('/')


class LoginHandler(BaseHandler):
    def get(self):

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("/login/login.html"))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)

        username = self.request.get("username", None)
        password = self.request.get("password", None)

        encoded_password = hashlib.sha1(password.encode('utf-8'))

        data = {
            "invalid_username": True
        }

        if username is None or password is None:
            self.response.write(jinja.render_template("login/login.html", **data))
            return

        user = User.query(User.username == username, User.password == encoded_password.hexdigest()).get()

        if user is None:
            self.response.write(jinja.render_template("login/login.html", **data))
            return

        self.session['user'] = user.username

        self.redirect('/')




