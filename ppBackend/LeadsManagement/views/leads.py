# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template

# Local imports
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.generic.services.utils import constants, decorators, common_utils

leads_bp = Blueprint("leads_bp", __name__)


@leads_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__LEAD,
    constants.OPTIONAL_FIELDS_LIST__LEAD,
)
def leads_create_view(data):
    res =  LeadsController.create_controller(data=data)
    return redirect(url_for('addlead_view'))


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