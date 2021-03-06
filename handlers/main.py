#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from models.snippet import Snippet
from models.user import User
from models.usersnippet import Rate
from webapp2_extras import jinja2, sessions
from handlers.register import RegisterHandler
from handlers.base import BaseHandler
from handlers.login import LoginHandler, LogoutHandler
from handlers.snippets \
    import CreateSnippetHandler, MySnippetsHandler, DeleteSnippetHandler, EditSnippetHandler,RateSnippetHandler


class MainHandler(BaseHandler):
    def get(self):
        snippets = Snippet.query().order(-Snippet.creation_date).fetch()
        session = self.session.get('user')
        is_logged = False
        logged_user = None
        if session is not None:
            is_logged = True
            logged_user = User.query(User.username == self.session.get('user')).get()


        for snippet in snippets:
            user = User.query(User.key == snippet.user).get()
            snippet.completeuser = user
            if logged_user:
                rate = Rate.query(Rate.snippet == snippet.key, Rate.user == logged_user.key).get()
                snippet.user_valoration = rate.positive_valoration if rate else None

        data = {
            "is_logged": is_logged,
            "snippets": snippets
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html", **data))


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'prepre',
}

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler),
    ('/logout', LogoutHandler),
    ('/login', LoginHandler),
    ('/newsnippet', CreateSnippetHandler),
    ('/mysnippets', MySnippetsHandler),
    ('/mysnippets/delete', DeleteSnippetHandler),
    ('/editsnippet', EditSnippetHandler),
    ('/rate', RateSnippetHandler)
], debug=True, config=config)
