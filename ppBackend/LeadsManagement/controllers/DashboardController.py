# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils
from ppBackend import config
from datetime import date


class DashboardController(Controller):
    Model = Leads

    @classmethod
    def read_lead(cls, data):
        user_childs = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        lead_dataset = []
        # queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **data})
        for user in user_childs:
            queryset = cls.db_read_records(read_filter={
                constants.CREATED_BY: user, **data})
            lead_dataset.append([user.name, len(queryset)])
        # lead_dataset.append(len(queryset))
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
        queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **data})
        user_childs = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        for user in user_childs:
            queryset = cls.db_read_records(read_filter={
                constants.CREATED_BY: user, **data})
            follow_dataset.append([user.name, [obj.display()
                                for obj in queryset]])
        for user in follow_dataset:
            calls = 0
            meetings = 0
            for follow in user[1]:
                if follow['type'] == 'Call':
                    calls += 1
                if follow['type'] == 'Meeting':
                    meetings += 1
            kpi_dataset.append([user[0], calls, meetings])
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=kpi_dataset
        )