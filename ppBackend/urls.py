# Python imports

# Framework imports
from flask import jsonify

# Local imports
from ppBackend import app
from ppBackend.generic.services.utils import constants
from ppBackend.UserManagement.views.users import users_bp
from ppBackend.LeadsManagement.views.leads import leads_bp


@app.route("/", methods=["GET"])
def index_view():
    return "Server is running fine."


@app.route("/api/static-data", methods=["GET"])
def static_data_view():
    return jsonify(constants.STATIC_DATA)


app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(leads_bp, url_prefix="/api/leads")
