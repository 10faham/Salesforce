# Python imports

# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.generic.services.utils import constants, decorators, common_utils

follow_ups_bp = Blueprint("follow_ups_bp", __name__)


@follow_ups_bp.route("/create", methods=["GET"])
@decorators.is_authenticated
def create_get_view():
    current_user = common_utils.current_user()
    return render_template('addfollow_up.html', leads=LeadsController.db_read_records({constants.CREATED_BY: current_user}))


@follow_ups_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__FOLLOW_UP,
    constants.OPTIONAL_FIELDS_LIST__FOLLOW_UP,
)
def create_view(data):
    leads = {}
    lead = LeadsController.db_read_single_record({constants.ID:data[constants.FOLLOW_UP__LEAD]})
    data[constants.FOLLOW_UP__ASSIGNED_TO] = lead[constants.LEAD__ASSIGNED_TO]
    res = FollowUpController.create_controller(data=data)
    leads[constants.LEAD__FOLLOWUP] = res['response_data'][constants.ID]
    leads[constants.ID] = data[constants.FOLLOW_UP__LEAD]
    leads[constants.LEAD__COMMENT] = res['response_data'][constants.FOLLOW_UP__COMMENT]
    leads[constants.LEAD__LEVEL] = res['response_data'][constants.FOLLOW_UP__LEVEL]
    leads[constants.LEAD__LAST_WORK] = res['response_data']['sub_type']
    leads[constants.LEAD__LAST_WORK_DATE] = res['response_data']['created_on']
    leads[constants.LEAD__FOLLOWUP_TYPE] = res['response_data']['type']
    leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = res['response_data']['next_deadline']
    leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = res['response_data']['next_task']
    leads[constants.LEAD__FOLLOWUP_REF_ID] = res['response_data']['follow_id']
    leads[constants.LEAD__PROJECT] = res['response_data']['next_project']
    leads[constants.LEAD__FOLLOWUP_COUNT] = lead['followup_count'] + 1

    res = LeadsController.db_update_single_record(read_filter = {constants.ID:data[constants.FOLLOW_UP__LEAD][constants.ID]}, update_filter = leads)
    return redirect(url_for('follow_ups_bp.read_view'))

@follow_ups_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__FOLLOW_UP,
)
def read_view(data):
    if request.method == "POST":
        data = request.form    
    res = FollowUpController.read_controller(data=data)
    return render_template("viewfollow_ups.html", **res)

@follow_ups_bp.route("/follow_read", methods=["POST","GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    # constants.REQUIRED_FIELDS_LIST__FOLLOW_UP_LEAD,
)
def readfp_view(data):
    data['lead'] = request.args.get('lead')
    data['name'] = request.args.get('name')
    data['ref'] = request.args.get('ref')
    # print(request.args.get('lead'))
    res = FollowUpController.read_lead_follow(data=data)
    return render_template("viewfollow_leads.html", **res)
