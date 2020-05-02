import webapp2
from webapp2_extras import jinja2, sessions


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session();

    def is_logged_user(self):
        session = self.session.get('user')
        is_logged = False
        if session is not None:
            is_logged = True
        return is_logged