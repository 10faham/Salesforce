# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from ppBackend.ClientsManagement.controllers.ClientsController import ClientsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, decorators, common_utils
from ppBackend.config import config

clients_bp = Blueprint("clients_bp", __name__)


@clients_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__CLIENTS,
    constants.REQUIRED_FIELDS_LIST__CLIENTS,
    request_form_data=False
)
def leads_create_view(data):
    rest = ClientsController.create_controller(data=data)
    return (rest)


@clients_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_view(data):
    if request.method == "POST":
        data = request.form
    res = ClientsController.read_controller(data=data)
    return render_template("viewleads.html", **res)


@clients_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def update_view(data):
    return ClientsController.update_controller(data=data)

@clients_bp.route("/search", methods=["POST", "GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def search_view(data):
    if request.method == "POST":
        data = request.form
        res = ClientsController.search_controller(data=data)
        return render_template("find_leads.html", **res)
    
    return render_template("find_leads.html")
