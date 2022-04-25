# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template

# Local imports
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
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
    rest = res
    data_follow['lead'] = res['response_data']['id']
    res = FollowUpController.create_controller(data=data_follow)
    # return redirect(url_for('addlead_view', **res))
    return render_template("./addlead.html", **res)
    # return render_template("./addfollow_up_bylead.html", **res)


@leads_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def read_view(data):
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
