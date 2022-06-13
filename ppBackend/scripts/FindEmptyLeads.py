# Date Created 14/09/2021 17:05:00


# Local imports
from asyncore import read
from ppBackend import app, config
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.generic.services.utils import constants, pipeline
from datetime import datetime

# from ppBackend.UserManagement.controllers.RoleController\
#     import RoleController


def find_empty_leads(run=False):
    if not run:
        return
    with app.test_request_context():
        count = 0
        # queryset = LeadsController.db_read_records(read_filter={}).aggregate(pipeline.ALL_LEADS)
        # empty_list = [obj for obj in queryset if obj['followup']['created_on'] == '']
        # # print(empty_list)
        # followup_data_new = {constants.FOLLOW_UP__COMMENT: 'LEAD RENEW',
        #     constants.FOLLOW_UP__COMPLETION_DATE: datetime.now().strftime(config.DATETIME_FORMAT), constants.FOLLOW_UP__NEXT_DEADLINE: datetime.now().strftime(config.DATETIME_FORMAT),
        #     constants.FOLLOW_UP__LEVEL: constants.FOLLOW_UP__LEVEL__LIST[2], constants.FOLLOW_UP__TYPE: 'Call',
        #     constants.FOLLOW_UP__SUB_TYPE: 'Call_attempt', constants.FOLLOW_UP__NEXT_TASK: 'ContactClient', constants.FOLLOW_UP__STATUS: 'Interested'}
        # for lead in empty_list:
        #     followup_data_new[constants.FOLLOW_UP__LEAD] = lead['_id']
        #     followup_data_new[constants.FOLLOW_UP__COMMENT] = 'LEAD RENEW FROM ' + lead['created_on']
        #     followup_data_new[constants.FOLLOW_UP__ASSIGNED_TO] = str(lead['user']['_id'])
        #     followup_data_new[constants.CREATED_BY] = '619b5af5a30ed6b97330addf'
        #     followup_data_new[constants.UPDATED_BY] = '619b5af5a30ed6b97330addf'
        #     res = FollowUpController.create_controller(data=followup_data_new)
        #     count += 1
        #     print(count)
        #     print(lead['_id'])

        queryset = FollowUpController.db_read_records(
            read_filter={constants.FOLLOWUP__ID+"__in": [str(num) for num in range(5369, 5801)]})
        for followUp in queryset:
            comment = followUp[constants.FOLLOW_UP__LEAD].fetch()[
                constants.LEAD__COMMENT]
            followUp[constants.FOLLOW_UP__COMMENT] = comment
            if comment:
                followUp.save()
            print(followUp.id)
