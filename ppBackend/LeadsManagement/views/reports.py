# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.LeadsManagement.controllers.DashboardController import DashboardController
from ppBackend.LeadsManagement.controllers.DashboardController import DashboardFollow
from ppBackend.generic.services.utils import constants, decorators, common_utils

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route("/kpisales", methods=["GET", "POST"])
@decorators.is_authenticated
@decorators.keys_validator()
def kpisales_view(data):
    if request.method == "POST":
        print(data.get(constants.DATE_FROM))
        print(request.form.get(constants.DATE_TO))
    
    res = DashboardController.read_lead_count(data=data)
    data = request.form
    res2 = DashboardFollow.read_kpi(data=data, data2=res)
    return render_template('kpisales.html', **res2)
