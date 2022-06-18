# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from ppBackend import config
from datetime import datetime


class ReportsController(Controller):
    Model = Leads

    @classmethod
    def read_lead_new(cls, data, filter={}):
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM)
            dateto = data.get(constants.DATE_TO)
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.LEAD__ASSIGNED_TO] = data.get(constants.ID)
            if data.get(constants.LEAD__TRANSFERED) == 'true':
                filter[constants.LEAD__TRANSFERED] = True
            else:
                filter[constants.LEAD__TRANSFERED] = False

        queryset = cls.db_read_records(read_filter={**filter}).aggregate(pipeline.ALL_LEADS)
        lead_data = [obj for obj in queryset]
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=lead_data
        )

    @classmethod
    def read_followup_new(cls, data, filter={}):
        user = common_utils.current_user()
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM)
            dateto = data.get(constants.DATE_TO)
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_BY] = data.get(constants.ID)
        if data.get('type') != 'Null':
            filter[constants.FOLLOW_UP__TYPE+"__in"] = data.get(constants.FOLLOW_UP__TYPE).split(',')
        if data.get('sub_type') != 'Null':
            filter[constants.FOLLOW_UP__SUB_TYPE+'__in'] = data.get(constants.FOLLOW_UP__SUB_TYPE).split(',')
        # queryset = FollowUpController.db_read_records(read_filter={**filter}).aggregate(pipeline.GET_LEADS_KPI)
        queryset = FollowUpController.db_read_records(read_filter={**filter})
        
        follow_up = [obj for obj in queryset]
        leads = []
        for obj in follow_up:
            leads.append({**obj['lead'], 'followup': obj, 'user':obj['user']})

        # leads.append([obj['lead'] for obj in follow_up])
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=leads
        )