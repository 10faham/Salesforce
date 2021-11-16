# Python imports

# Framework imports
from flask import Blueprint

# Local imports
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, decorators, common_utils

users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__USER,
    constants.OPTIONAL_FIELDS_LIST__USER,
)
def create_view(data):
    return UserController.create_controller(data=data)


@users_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__USER,
)
def read_view(data):
    return UserController.read_controller(data=data)


@users_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__USER,
)
def update_view(data):
    return UserController.update_controller(data=data)


@users_bp.route("/login", methods=["POST"])
@decorators.logging
@decorators.keys_validator(constants.LOGIN_REQUIRED_FIELDS_LIST, [])
def login_user_view(data):
    return UserController.login_controller(data=data)

@users_bp.route("/logout", methods=["PATCH"])
@decorators.logging
@decorators.is_authenticated
@decorators.keys_validator()
def logout_user_view(_):
    return UserController.logout_controller()
