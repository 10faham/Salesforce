# Python imports

# Framework imports

# Local imports
from ast import Constant
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.LeadHistory import LeadHistory
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from ppBackend import config
from datetime import datetime


class LeadsHistoryController(Controller):
    Model = LeadHistory

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        _, _, obj = cls.db_insert_record(
            data=data, default_validation=False)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )

    @classmethod
    def read_controller(cls, data):
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
        
        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.LEAD__ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)

        user_ids = [id[constants.ID] for id in user_childs]
        filter[constants.LEAD__ASSIGNED_TO+"__in"] = [str(id) for id in user_ids]
        queryset = cls.db_read_records(read_filter={**filter}).aggregate(pipeline.ALL_LEADS)

        lead_dataset = [obj for obj in queryset]
        # lead_data = {}
        # lead_id = []
        # for obj in queryset.order_by('-'+constants.CREATED_ON):
        #     lead_id.append(str(obj[constants.ID]))
        #     lead_data[str(obj[constants.ID])] = {'data': obj.display_min()}
        #     # counter = 0
        # # final_count = 0
        # # for id in lead_id:
        # #     followup = FollowUpController.read_count(id)
        # #     if followup["count"] > 0:
        # #         final_count += 1
        # # print(final_count)
        # # for i in range(0, len(lead_id), 100):
        # followup = FollowUpController.read_current_followup(lead_id)
        # for obj in followup:
        #     lead_data[obj['_id']].update({'followup': obj})

        # for obj in queryset.order_by("-"+constants.CREATED_ON):
        #     tmp = obj.display()
        #     tmp['followup'] = FollowUpController.read_count(tmp['id'])
        #     lead_data.append(tmp)
        
        # lead_dataset.append(
            # [str(user.pk), user[constants.USER__NAME], lead_data])
        # lead_dataset.append(common_utils.current_user().name)
        temp = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        all_users = []
        for id in temp:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        leads_data = {}
        leads_data['data'] = lead_dataset
        leads_data['username'] = common_utils.current_user()[
            constants.USER__NAME]
        leads_data['all_users'] = all_users
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=leads_data
        )
