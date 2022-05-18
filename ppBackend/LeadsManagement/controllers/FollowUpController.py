# Python imports

# Framework imports

# Local imports
from datetime import datetime, timedelta
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.UserManagement.controllers.UserController import UserController
# from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils
from ppBackend import config


class FollowUpController(Controller):
    Model = FollowUp

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages, data = cls.cls_validate_data(data=data,
                                                               return_data=True)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        # if common_utils.get_time() > common_utils.convert_to_epoch(data[constants.FOLLOW_UP__NEXT]):
        #     return response_utils.get_response_object(
        #         response_code=response_codes.CODE_WRONG_PARAMETERS,
        #         response_message=response_codes.MESSAGE_HAS_TO_BE_LESS_THAN.format(
        #             constants.FOLLOW_UP__NEXT, constants.CURRENT_TIME
        #         ))
        # if data[constants.FOLLOW_UP__LEAD][constants.CREATED_BY] != common_utils.current_user():
        #     return response_utils.get_response_object(
        #         response_code=response_codes.CODE_UNAUTHENTICATED_ACCESS,
        #         response_message=response_codes.MESSAGE_UNAUTHENTICATED_ACCESS
        #     )
        # data[constants.FOLLOW_UP__LEAD][constants.LEAD__STATUS] = data[constants.FOLLOW_UP__STATUS]
        # data[constants.FOLLOW_UP__LEAD].save()
        _, _, obj = cls.db_insert_record(data=data)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )

    @classmethod
    def read_controller(cls, data):
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM).split('T')
            dateto = data.get(constants.DATE_TO).split('T')
            filter[constants.FOLLOW_UP__NEXT_DEADLINE+"__gte"] = datetime.strptime(datefrom[0], config.DATE_FORMAT)
            filter[constants.FOLLOW_UP__NEXT_DEADLINE+"__lte"] = datetime.strptime(dateto[0], config.DATE_FORMAT)
        
        user_childs = UserController.get_user_childs(user=common_utils.current_user(),
                                                     return_self=True)
        followup_dataset = []
        followup_data = {}
        overdue = []
        today = []
        tomorrow = []
        next7 = []
        all = []
        for user in user_childs:
            queryset = cls.db_read_records(
                read_filter={constants.CREATED_BY: user, **filter})
            tmp = []
            tmp.append([obj.display() for obj in queryset])
            leads_id = []
            for lead in tmp:
                for follow in lead:
                    if follow[constants.FOLLOW_UP__LEAD][constants.ID] not in leads_id:
                        leads_id.append(follow[constants.FOLLOW_UP__LEAD][constants.ID])
            
            tmp_follow = [FollowUpController.read_count(obj) for obj in leads_id]
            for item in tmp_follow:
                # print(datetime.now().date())
                # print(item['data']['next_deadline'].date())
                now = datetime.now().date()
                if item['data'][constants.FOLLOW_UP__NEXT_DEADLINE].date() < now:
                    overdue.append(item)
                if item['data'][constants.FOLLOW_UP__NEXT_DEADLINE].date() == now:
                    today.append(item)
                if item['data'][constants.FOLLOW_UP__NEXT_DEADLINE].date() == (now + timedelta(days = 1)):
                    tomorrow.append(item)
                if item['data'][constants.FOLLOW_UP__NEXT_DEADLINE].date() > now and item[
                    'data'][constants.FOLLOW_UP__NEXT_DEADLINE].date() <= (now + timedelta(days = 7)):
                    next7.append(item)
                all.append(item)
            followup_dataset.append([user.name, tmp, tmp_follow])

            # for obj in queryset:
            #     tmp = obj.display()
            #     # tmp['followup'] = FollowUpController.read_count(tmp['id'])
            #     lead_data.append(FollowUpController.read_count(['id']))
            # lead_dataset.append(
            #     [str(user.pk), user[constants.USER__NAME], lead_data])
        user = common_utils.current_user()
        followup_data['followup'] = followup_dataset
        followup_data['overdue'] = overdue
        followup_data['today'] = today
        followup_data['tomorrow'] = tomorrow
        followup_data['next7'] = next7
        followup_data['all'] = all
        followup_data['usernamne'] = common_utils.current_user()[constants.USER__NAME]
        # followup_dataset.append(user.name)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=followup_data
        )

    @classmethod
    def read_count(cls, lead_id):
        queryset = cls.db_read_records(
            read_filter={constants.FOLLOW_UP__LEAD: lead_id})
        followup = {'count': queryset.count()}
        followup['data'] = queryset.order_by(
            "-"+constants.CREATED_ON).first() or {}
        if followup["data"]:
            followup["data"] = followup["data"].display()
        return followup

    @classmethod
    def suspend_controller(cls, data):
        current_user = common_utils.current_user()
        filter = {}
        if current_user[constants.USER__ROLE] != constants.DEFAULT_ADMIN_ROLE_OBJECT:
            filter = {constants.CREATED_BY: current_user}
        _, _, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID], **filter}, update_filter={
                constants.STATUS: constants.OBJECT_STATUS_SUSPENDED},
            update_mode=constants.UPDATE_MODE__PARTIAL,
        )
        if obj:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display(),
            )
        return response_utils.get_response_object(
            response_code=response_codes.CODE_RECORD_NOT_FOUND,
            response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                constants.FOLLOW_UP.title(), constants.ID
            ))

    @classmethod
    def read_lead_follow(cls, data):
        queryset = cls.db_read_records(
            read_filter={constants.FOLLOW_UP__LEAD: data['lead']})
        user = common_utils.current_user()
        followup_dataset = [obj.display() for obj in queryset]
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=followup_dataset
        )
