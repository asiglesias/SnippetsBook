#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from webapp2_extras import jinja2
import hashlib
from models.user import User
from handlers.base import BaseHandler


class RegisterHandler(BaseHandler):
    def get(self):

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("register/register.html"))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)
        username = self.request.get("username", None)
        email = self.request.get("email", None)
        password = self.request.get("password", None)

        if username is None or email is None or password is None:
            self.response.write(jinja.render_template("register/register.html"))
            return


        key = hashlib.sha1(password.encode('utf-8'))

        query = User.query(User.username == username).fetch()
        if len(query) > 0:
            self.response.write(jinja.render_template("register/register.html"))
            return

        registered_user = User(username=username, email=email, password=key.hexdigest())
        k = registered_user.put()

        self.session['user'] = registered_user.username
        self.redirect('/')

