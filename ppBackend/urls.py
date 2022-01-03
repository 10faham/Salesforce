# Python imports

# Framework imports
from flask import jsonify
from flask import render_template, redirect, request, Response

# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.generic.services.utils import constants, decorators
from ppBackend.UserManagement.views.users import users_bp
from ppBackend.LeadsManagement.views.leads import leads_bp
from ppBackend.LeadsManagement.views.follow_ups import follow_ups_bp
from ppBackend.generic.services.utils import common_utils
from ppBackend.generic.services.utils.common_utils import current_user


# @app.route("/", methods=["GET"])
# def index_view():
#     return render_template('login.html')
# return "Server is running fine."

@app.route("/home", methods=["GET"])
@decorators.logging
@decorators.is_authenticated
def dashboard_view():
    return render_template('dashboard.html')


@app.route("/addlead", methods=["GET"])
def addlead_view():
    return render_template('addlead.html')


@app.route("/api/static-data", methods=["GET"])
def static_data_view():
    return jsonify(constants.STATIC_DATA)


app.register_blueprint(users_bp, url_prefix="/")
app.register_blueprint(leads_bp, url_prefix="/api/leads")
app.register_blueprint(follow_ups_bp, url_prefix="/api/follow_ups")
