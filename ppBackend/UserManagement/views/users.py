# Python imports

# Framework imports
from flask import Blueprint, render_template, request

# Local imports
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, decorators, response_codes, response_utils


users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/create", methods=["GET"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator()
def create_viewget(data):
    return render_template("adduser.html")


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
    res = UserController.read_controller(data=data)
    return render_template("view_user.html", **res)


@users_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__USER,
)
def update_view(data):
    return UserController.update_controller(data=data)

@users_bp.route("/suspend", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    []
)
def suspend_view(data):
    data = request.form
    res = UserController.suspend_controller(data=data)
    return render_template("view_user.html", **res)

@users_bp.route("/", methods=["GET"])
@decorators.logging
@decorators.keys_validator()
def logined_user_view(data):
    return render_template("login.html", Response=response_utils.get_response_object())


@users_bp.route("/", methods=["POST"])
@decorators.logging
@decorators.keys_validator(constants.LOGIN_REQUIRED_FIELDS_LIST, [])
def login_user_view(data):
    res = UserController.login_controller(data=data)
    return render_template("login.html", **res)
    # if res['response_code'] != response_codes.CODE_SUCCESS:
    #     return redirect(url_for('dashboard_view'), Response=res)
    # else:
    #     return render_template("failed.html", Response=res)


@users_bp.route("/logout", methods=["PATCH"])
@decorators.logging
@decorators.is_authenticated
@decorators.keys_validator()
def logout_user_view(_):
    return UserController.logout_controller()
