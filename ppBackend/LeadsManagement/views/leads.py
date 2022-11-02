# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, decorators, common_utils
from ppBackend.config import config

leads_bp = Blueprint("leads_bp", __name__)


@leads_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__LEAD_FOLLOWUP,
    constants.OPTIONAL_FIELDS_LIST__LEAD_FOLLOWUP,
    request_form_data=False
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
    data_lead[constants.LEAD__FOLLOWUP_COUNT] = 1
    rest = LeadsController.create_controller(data=data_lead)
    if rest['response_code'] == 200:
        data_follow['lead'] = rest['response_data']['id']
        data_follow[constants.FOLLOW_UP__ASSIGNED_TO] = common_utils.current_user()
        res = FollowUpController.create_controller(data=data_follow)
        leads = {}
        leads[constants.LEAD__FOLLOWUP] = res['response_data'][constants.ID]
        leads[constants.ID] = res['response_data'][constants.FOLLOW_UP__LEAD]['id']
        leads[constants.LEAD__COMMENT] = res['response_data'][constants.FOLLOW_UP__COMMENT]
        leads[constants.LEAD__LEVEL] = res['response_data'][constants.FOLLOW_UP__LEVEL]
        leads[constants.LEAD__LAST_WORK] = res['response_data']['sub_type']
        leads[constants.LEAD__LAST_WORK_DATE] = res['response_data']['created_on']
        leads[constants.LEAD__FOLLOWUP_TYPE] = res['response_data']['type']
        leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = res['response_data']['next_deadline']
        leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = res['response_data']['next_task']
        leads[constants.LEAD__PROJECT] = res['response_data']['next_project']
        res = LeadsController.db_update_single_record(read_filter = {constants.ID:res['response_data'][constants.FOLLOW_UP__LEAD]['id']}, update_filter = leads)

    # return redirect(url_for('addlead_view', **res))
    return (rest)
    # return render_template("./addfollow_up_bylead.html", **res)


@leads_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator()
def read_view(data):
    if request.method == "POST":
        data = request.form
        res = LeadsController.read_controller(data=data)
        return res    
    data = request.args
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
# @decorators.keys_validator(constants request_form_data=False)
def lead_transfer():
    data = request.form
    res = LeadsController.lead_transfer(data=data)
    return res

@leads_bp.route("/bulkadd", methods=["GET", "POST"])
@decorators.is_authenticated
# @decorators.keys_validator()
def lead_bulk_add():
    duplicates = []
    failed = []
    if request.method == "POST":
        uploaded_file = request.files['file']
        data = request.form
        datafile = pd.read_csv(uploaded_file)
        jout = datafile.to_dict(orient="split")
        unique = []
        lead = {}
        for index, item in enumerate(jout['data']):
            tmp = [] 
            if item[1] != item[1]:
                item[1] = ''
            if item[2] == item[2]:
                tmp.append(item[2][2:-2])
                item[2] = tmp
                # item[2] = item[2].replace(".", "")
                # item[2] = item[2].replace(" ", "")
                # item[2] = re.sub('^00', '+', item[2])
                # item[2] = re.sub('^03', '+923', item[2])
                # item[2] = re.sub('^3', '+923', item[2])
                # queryset = LeadsController.db_read_records(read_filter={constants.LEAD__PHONE_NUMBER+"__in": item[2]})
                # if queryset:
                #     duplicates.append(index)
                # else:
                unique.append(item)
                print(item)
                for index, header in enumerate(jout["columns"]):
                    lead[header] = item[index]
                data_lead = {
                    key: lead[key] for key in [*constants.REQUIRED_FIELDS_LIST__LEAD,
                                            *constants.OPTIONAL_FIELDS_LIST__LEAD] if lead.get(key)
                }
                data_follow = {
                    key: lead[key] for key in [*constants.REQUIRED_FIELDS_LIST__FOLLOW_UP,
                                            *constants.OPTIONAL_FIELDS_LIST__FOLLOW_UP] if lead.get(key)
                }
                data_lead[constants.LEAD__FOLLOWUP_COUNT] = 1
                rest = LeadsController.create_controller(data=data_lead)
                if rest['response_code'] != 200:
                    failed.append(index)
                if rest['response_code'] == 200:
                    data_follow['lead'] = rest['response_data']['id']
                    data_follow[constants.FOLLOW_UP__ASSIGNED_TO] = common_utils.current_user()
                    data_follow[constants.FOLLOW_UP__COMPLETION_DATE] = datetime.now().strftime(config.DATETIME_FORMAT)
                    data_follow[constants.FOLLOW_UP__NEXT_DEADLINE] = datetime.now().strftime(config.DATETIME_FORMAT)
                    res = FollowUpController.create_controller(data=data_follow)
                    leads = {}
                    leads[constants.LEAD__ASSIGNED_TO] = data[constants.LEAD__ASSIGNED_TO]
                    leads[constants.LEAD__FOLLOWUP] = res['response_data'][constants.ID]
                    leads[constants.ID] = res['response_data'][constants.FOLLOW_UP__LEAD]['id']
                    leads[constants.LEAD__COMMENT] = res['response_data'][constants.FOLLOW_UP__COMMENT]
                    leads[constants.LEAD__LEVEL] = res['response_data'][constants.FOLLOW_UP__LEVEL]
                    leads[constants.LEAD__LAST_WORK] = res['response_data']['sub_type']
                    leads[constants.LEAD__LAST_WORK_DATE] = res['response_data']['created_on']
                    leads[constants.LEAD__FOLLOWUP_TYPE] = res['response_data']['type']
                    leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = res['response_data']['next_deadline']
                    leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = res['response_data']['next_task']
                    leads[constants.LEAD__PROJECT] = res['response_data']['next_project']
                    leads[constants.LEAD__ASSIGNED_BY] = common_utils.current_user()
                    leads[constants.LEAD__TRANSFERED] = True
                    leads[constants.LEAD__TRANSFERED_ON] = common_utils.get_time()
                    res = LeadsController.db_update_single_record(read_filter = {constants.ID:res['response_data'][constants.FOLLOW_UP__LEAD]['id']}, update_filter = leads)
    temp = UserController.get_user_childs(
        user=common_utils.current_user(), return_self=True)
    all_users = []
    print(len(duplicates))
    print(len(failed))
    for id in temp:
        all_users.append([str(id[constants.ID]), id[constants.USER__NAME]])
    response_data = {'all_users': all_users, 'duplicate':len(duplicates)}
    return render_template("leadbulkadd.html", **response_data)
