# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils
from ppBackend import config
from datetime import datetime


class DashboardController(Controller):
    Model = Leads

    @classmethod
    def read_lead(cls, data):
        user_childs = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        lead_dataset = []
        temp = []
        for user in user_childs:
            if user == common_utils.current_user():
                queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user})
                lead_dataset.append([user.name, len(queryset)])
            else:
                queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user})
                temp.append([user.name, len(queryset)])
        for each in temp:
            lead_dataset.append(each)

        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=lead_dataset
        )

class DashboardFollow(Controller):
    Model = FollowUp

    @classmethod
    def read_follow(cls, data):
        user = common_utils.current_user()
        follow_dataset = []
        queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **data})

        follow_dataset.append([len(queryset)])
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=follow_dataset
        )

    @classmethod
    def read_kpi(cls, data):
        user = common_utils.current_user()
        follow_dataset = []
        kpi_dataset = []
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM).split('T')
            dateto = data.get(constants.DATE_TO).split('T')
            filter[constants.FOLLOW_UP__COMPLETION_DATE+"__gte"] = datetime.strptime(datefrom[0], '%Y-%m-%d')
            filter[constants.FOLLOW_UP__COMPLETION_DATE+"__lte"] = datetime.strptime(dateto[0], '%Y-%m-%d')

        # queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **filter, **data})
        user_childs = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        temp = []
        for user in user_childs:
            if user == common_utils.current_user():
                queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **filter})
                follow_dataset.append([user.name, [obj.display() for obj in queryset]])
            else:
                queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **filter})
                temp.append([user.name, [obj.display() for obj in queryset]])
        for each in temp:
            follow_dataset.append(each)
        
        for user in follow_dataset:
            calls = 0
            meetings = 0
            at_calls = 0
            v_calls = 0
            for follow in user[1]:
                if follow['type'] == 'Call':
                    calls += 1
                if follow['type'] == 'Meeting':
                    meetings += 1
                if follow['sub_type'] == 'Contacted_client' or "Followed_up" or "Whatsapp_call" or "Meeting_Confirmed" or 'Meeting_cancelled' or "Meeting_postponed":
                    v_calls += 1
                if follow['sub_type'] == 'Call_attempt':
                    at_calls += 1
            kpi_dataset.append([user[0], calls, meetings, len(user[1]), at_calls, v_calls])
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=kpi_dataset
        )