# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, decorators, common_utils

leads_bp = Blueprint("leads_bp", __name__)


@leads_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__LEAD_FOLLOWUP,
    constants.OPTIONAL_FIELDS_LIST__LEAD_FOLLOWUP,
)
def leads_create_view(data):
    # data_lead = {}
    # data_follow = {}
    # for key in constants.REQUIRED_FIELDS_LIST__LEAD:
    #     if key in data:
    #         data_lead[key] = data[key]
    # for key in constants.OPTIONAL_FIELDS_LIST__LEAD:
    #     if key in data:
    #         data_lead[key] = data[key]
    data_lead = {
        key: data[key] for key in [*constants.REQUIRED_FIELDS_LIST__LEAD,
                                   *constants.OPTIONAL_FIELDS_LIST__LEAD] if data.get(key)
    }
    data_follow = {
        key: data[key] for key in [*constants.REQUIRED_FIELDS_LIST__FOLLOW_UP,
                                   *constants.OPTIONAL_FIELDS_LIST__FOLLOW_UP] if data.get(key)
    }
    # for key in constants.REQUIRED_FIELDS_LIST__FOLLOW_UP:
    #     if key in data:
    #         data_follow[key] = data[key]
    # for key in constants.OPTIONAL_FIELDS_LIST__FOLLOW_UP:
    #     if key in data:
    #         data_follow[key] = data[key]

    res = LeadsController.create_controller(data=data_lead)
    if res['response_code'] == 200:
        data_follow['lead'] = res['response_data']['id']
        data_follow[constants.FOLLOW_UP__ASSIGNED_TO] = common_utils.current_user()
        res = FollowUpController.create_controller(data=data_follow)
    # return redirect(url_for('addlead_view', **res))
    return render_template("./addlead.html", **res)
    # return render_template("./addfollow_up_bylead.html", **res)


@leads_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator()
def read_view(data):
    if request.method == "POST":
        data = request.form
    res = LeadsController.read_controller(data=data)
    return render_template("viewleads.html", **res)


@leads_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def update_view(data):
    return LeadsController.update_controller(data=data)

@leads_bp.route("/search", methods=["POST", "GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def search_view(data):
    if request.method == "POST":
        data = request.form
        res = LeadsController.search_controller(data=data)
        return render_template("find_leads.html", **res)
    
    return render_template("find_leads.html")

@leads_bp.route("/bulktransfer", methods=["POST", "GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def bulk_trasnfer(data):
    if request.method == "POST":
        data = request.form
        res = LeadsController.bulk_transfer(data=data)
        return render_template("bulkleads.html", **res)
    
    res = UserController.get_users_childs_list(data)
    return render_template("bulkleads.html", **res)

@leads_bp.route("/leadtransfer", methods=["POST"])
@decorators.is_authenticated
# @decorators.keys_validator()
def lead_transfer():
    data = request.form
    res = LeadsController.lead_transfer(data=data)
    return res