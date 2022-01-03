# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template

# Local imports
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.generic.services.utils import constants, decorators, common_utils

leads_bp = Blueprint("leads_bp", __name__)


@leads_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__FOLLOW_UP,
    constants.OPTIONAL_FIELDS_LIST__FOLLOW_UP,
)
def leads_create_view(data):
    res = FollowUpController.create_controller(data=data)
    return render_template("./addlead.html", **res)


@leads_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__FOLLOW_UP,
)
def read_view(data):
    res = FollowUpController.read_controller(data=data)
    return render_template("viewleads.html", **res)
