# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.UserManagement.controllers.UserController import UserController
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
        if data[constants.FOLLOW_UP__LEAD][constants.CREATED_BY] != common_utils.current_user():
            return response_utils.get_response_object(
                response_code=response_codes.CODE_UNAUTHENTICATED_ACCESS,
                response_message=response_codes.MESSAGE_UNAUTHENTICATED_ACCESS
            )
        data[constants.FOLLOW_UP__LEAD][constants.LEAD__STATUS] = data[constants.FOLLOW_UP__STATUS]
        data[constants.FOLLOW_UP__LEAD].save()
        _, _, obj = cls.db_insert_record(data=data)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )

    @classmethod
    def read_controller(cls, data):
        user_childs = UserController.get_user_childs(user=common_utils.current_user(),
                                                     return_self=True)
        followup_dataset = []
        temp = []
        for user in user_childs:
            if user == common_utils.current_user():
                queryset = cls.db_read_records(
                    read_filter={constants.CREATED_BY: user, **data})
                followup_dataset.append(
                    [user.name, [obj.display() for obj in queryset]])
            else:
                queryset = cls.db_read_records(
                    read_filter={constants.CREATED_BY: user, **data})
                temp.append([user.name, [obj.display() for obj in queryset]])
        for each in temp:
            followup_dataset.append(each)
        user = common_utils.current_user()
        # followup_dataset.append(user.name)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=followup_dataset
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
        followup_dataset = []
        user = common_utils.current_user()
        followup_dataset.append([obj.display() for obj in queryset])
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=followup_dataset
        )
