#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from models.snippet import Snippet
from webapp2_extras import jinja2


class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("register/register.html"))


