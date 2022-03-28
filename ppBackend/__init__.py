# Framework imports
from flask import Flask
from flask import render_template
from flask_moment import Moment
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
# Local imports
from ppBackend.generic.database import initialize_db
from ppBackend.config import config


# application objects
app = Flask(__name__)
CORS(app)
app.config["MONGODB_HOST"] = config.MONGO_DB_URI
initialize_db(app)
moment = Moment(app)
bcrypt = Bcrypt(app)
app.config.update(config.MAIL_SETTINGS)
# from ppBackend.scripts import run_scripts
# run_scripts()
# Routing
import ppBackend.urls