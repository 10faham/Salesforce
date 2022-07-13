# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.LeadsManagement.controllers.DashboardController import DashboardController
from ppBackend.LeadsManagement.controllers.DashboardController import DashboardFollow
from ppBackend.LeadsManagement.controllers.ReportsController import ReportsController
from ppBackend.generic.services.utils import constants, decorators, common_utils

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route("/kpisales", methods=["GET", "POST"])
@decorators.is_authenticated
@decorators.keys_validator()
def kpisales_view(data):
    if request.method == "POST":
        data = request.form
        print(data.get(constants.DATE_FROM))
        print(data.get(constants.DATE_TO))
    data = request.form
    res = DashboardController.read_lead_count(data=data)
    data = request.form
    res2 = DashboardFollow.read_kpi(data=data, data2=res)
    return render_template('kpisales.html', **res2)

@reports_bp.route("/detailed", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator([constants.ID, 'datefrom', 'dateto', constants.LEAD__TRANSFERED], request_form_data=False)
def read_lead_new(data):
    data[constants.DATE_TO] = data["dateto"]
    data[constants.DATE_FROM] = data["datefrom"]
    res = ReportsController.read_lead_new(data=data)
    return render_template('kpileads.html', **res)

@reports_bp.route("/detailed-follow", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_followup_new(data):
    data[constants.ID] = request.args.get('id')
    data[constants.DATE_FROM] = request.args.get('datefrom')
    data[constants.DATE_TO] = request.args.get('dateto')
    data[constants.LEAD__TRANSFERED] = request.args.get('transfered')
    data[constants.FOLLOW_UP__TYPE] = request.args.get('filter')
    data[constants.FOLLOW_UP__SUB_TYPE] = request.args.get('sub-filter')
    res = ReportsController.read_followup_new(data=data)
    return render_template('kpileads.html', **res)