# Framework imports
from flask import Flask
from flask_moment import Moment
from flask_cors import CORS
from flask_bcrypt import Bcrypt
# Local imports
from ppBackend.generic.database import initialize_db
from ppBackend.config import config


def register_scripts():
    from ppBackend.scripts import run_scripts
    run_scripts(execute_create_admin_user_if_not_exists=False,
                execute_phone_number_format_correction=False)
    # Routing
    import ppBackend.urls


# application objects
app = Flask(__name__)
CORS(app)
app.config["MONGODB_HOST"] = config.MONGO_DB_URI
initialize_db(app)
moment = Moment(app)
bcrypt = Bcrypt(app)
app.config.update(config.MAIL_SETTINGS)
register_scripts()
