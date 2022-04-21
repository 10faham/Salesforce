# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils
from ppBackend import config


class LeadsController(Controller):
    Model = Leads

    @classmethod
    def create_controller(cls, data):
        print(data)
        is_valid, error_messages, obj = cls.db_insert_record(
            data=data, db_commit=False)
        if is_valid:
            logged_in_user = common_utils.current_user()
            already_exists = cls.db_read_records(read_filter={
                constants.LEAD__PHONE_NUMBER: obj[constants.LEAD__PHONE_NUMBER],
                constants.CREATED_BY+"__nin": [logged_in_user]
            })
            if already_exists:
                # TODO
                print('duplicate number**********************************')
                return response_utils.get_response_object(
                    response_code=response_codes.CODE_USER_ALREADY_EXIST,
                    response_message=response_codes.MESSAGE_ALREADY_EXISTS_DATA,
                    response_data=already_exists
                )
            obj.save()
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display()
            )
        print('validation failed ********************************')
        print(error_messages)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_VALIDATION_FAILED,
            response_message=response_codes.MESSAGE_VALIDATION_FAILED,
            response_data=error_messages
        )

    @classmethod
    def read_controller(cls, data):
        user_childs = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        lead_dataset = []
        for user in user_childs:
            queryset = cls.db_read_records(read_filter={
                constants.CREATED_BY: user, **data})
            lead_dataset.append([user.name, [obj.display()
                                for obj in queryset]])
        lead_dataset.append(common_utils.current_user().name)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=lead_dataset
        )

    @classmethod
    def update_controller(cls, data):
        is_valid, error_messages, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]}, update_filter=data
        )
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if not obj:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.LEAD.title(), constants.ID
                ))
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display(),
        )

    @classmethod
    def suspend_controller(cls, data):
        _, _, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]},
            update_filter={
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
                constants.LEAD.title(), constants.ID
            ))
