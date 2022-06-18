# Python imports

# Framework imports
from flask import jsonify
from flask import render_template, redirect, request, Response
from datetime import datetime, timedelta

# Local imports
from ppBackend import app, config
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.generic.services.utils import constants, decorators
from ppBackend.UserManagement.views.users import users_bp
from ppBackend.LeadsManagement.views.leads import leads_bp
from ppBackend.LeadsManagement.views.follow_ups import follow_ups_bp
from ppBackend.LeadsManagement.views.reports import reports_bp
from ppBackend.generic.services.utils import common_utils
from ppBackend.generic.services.utils.common_utils import current_user
from ppBackend.LeadsManagement.controllers.DashboardController import DashboardController
from ppBackend.LeadsManagement.controllers.DashboardController import DashboardFollow


# @app.route("/", methods=["GET"])
# def index_view():
#     return render_template('login.html')
# return "Server is running fine."

@app.route("/home", methods=["GET"])
# @decorators.logging
@decorators.is_authenticated
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def dashboard_view(data):
    data = {
        constants.LEAD__ASSIGNED_TO: common_utils.current_user()[
            constants.ID]
    }
    res = DashboardController.read_lead_count(data=data)
    res2 = DashboardFollow.read_follow(data=data)
    obj = {'leads_count':'0',
        'follow_ups':'0'}
    obj.update({'leads_count':res})
    obj.update({'follow_ups':res2})
    return render_template('dashboard.html', **obj)


@app.route("/addlead", methods=["GET"])
def addlead_view():
    return render_template('addlead.html')

@app.route("/api/static-data", methods=["GET"])
def static_data_view():
    return jsonify(constants.STATIC_DATA)


app.register_blueprint(users_bp, url_prefix="/")
app.register_blueprint(leads_bp, url_prefix="/api/leads")
app.register_blueprint(follow_ups_bp, url_prefix="/api/follow_ups")
app.register_blueprint(reports_bp, url_prefix="/api/reports")
