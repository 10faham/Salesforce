# Date Created 22/05/2022 00:00:00


# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
from ppBackend.config import config
from ppBackend.generic.services.utils import common_utils, constants, pipeline
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController

# from ppBackend.UserManagement.controllers.RoleController\
#     import RoleController


def update_leads(run=False):
    if not run:
        return
    with app.test_request_context():
        # count = 0
        leads= {}
        queryset = LeadsController.db_read_records(read_filter={}, deleted_records=True).aggregate(pipeline.ALL_LEADS_DATA)
        all_leads = list(queryset)
        for lead in all_leads:
            print(lead)
            try:
                leads[constants.ID] = lead['_id']
                leads[constants.LEAD__FOLLOWUP] = lead['followup']['id']
                leads[constants.LEAD__COMMENT] = lead['followup']['comment']
                leads[constants.LEAD__LEVEL] = lead['followup']['level']
                leads[constants.LEAD__LAST_WORK] = lead['followup']['sub_type']
                leads[constants.LEAD__FOLLOWUP_TYPE] = lead['followup']['type']
                leads[constants.LEAD__LAST_WORK_DATE] = lead['followup']['created_on']
                leads[constants.LEAD__FOLLOWUP_COUNT] = lead['followup']['follow_count']
                leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = lead['followup']['next_deadline']
                leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = lead['followup']['next_task']
                leads[constants.LEAD__FOLLOWUP_REF_ID] = lead['followup']['follow_id']
                res = LeadsController.db_update_single_record(read_filter = {constants.ID:lead['_id']}, update_filter = leads, deleted_records = True)
                print(res)
            except Exception as e:
                print(e)