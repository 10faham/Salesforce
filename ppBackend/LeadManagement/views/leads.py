# Python imports

# Framework imports
from flask import Blueprint

# Local imports
from ppBackend.LeadManagement.controllers.LeadController import LeadController
from ppBackend.generic.services.utils import constants, decorators, common_utils

leads_bp = Blueprint("leads_bp", __name__)


@leads_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__LEAD,
    constants.OPTIONAL_FIELDS_LIST__LEAD,
)
def create_view(data):
    return LeadController.create_controller(data=data)


@leads_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def read_view(data):
    return LeadController.read_controller(data=data)


@leads_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def update_view(data):
    return LeadController.update_controller(data=data)