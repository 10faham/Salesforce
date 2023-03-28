# Python imports

# Framework imports

# Local imports
from ppBackend import config
from ppBackend.UserManagement.models.User import User
from ppBackend.generic.controllers import Controller
from ppBackend.UserManagement.controllers.TokenController import TokenController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils


class UserController(Controller):
    Model = User

    @classmethod
    def create_controller(cls, data):
        data[constants.USER__ROLE] = constants.DEFAULT_ROLE_OBJECTS[int(data[constants.USER__ROLE])]
        user_manager = cls.db_read_single_record(read_filter={constants.USER__NAME : data[constants.USER__MANAGER]})
        data[constants.USER__MANAGER] = user_manager[constants.ID]
        is_valid, error_messages, obj = cls.db_insert_record(
            data=data, db_commit=False)
        if is_valid:
            obj[constants.USER__PASSWORD] = common_utils.encrypt_password(
                password=obj[constants.USER__PASSWORD])
            obj.save()
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display()
            )
        return response_utils.get_response_object(
            response_code=response_codes.CODE_VALIDATION_FAILED,
            response_message=response_codes.MESSAGE_VALIDATION_FAILED,
            response_data=error_messages
        )

    @classmethod
    def read_controller(cls, data):
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=[
                obj.display() for obj in cls.db_read_records(read_filter=data)
            ])

    @classmethod
    def update_controller(cls, data):
        if data[constants.USER__PASSWORD]:
            data[constants.USER__PASSWORD] = common_utils.encrypt_password(
                password=data[constants.USER__PASSWORD])
        is_valid, error_messages, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]}, update_filter=data, default_validation=False
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
                    constants.USER.title(), constants.ID
                ))
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display(),
        )

    @classmethod
    def suspend_controller(cls, data):
        _, _, obj = cls.db_update_single_record(
            read_filter=data[constants.ID],
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
                constants.USER.title(), constants.ID
            ))

    @classmethod
    def login_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data,
                                                         validation_rules=cls.Model.login_validation_rules())
        if is_valid:
            user = cls.db_read_single_record(read_filter={
                constants.USER__EMAIL_ADDRESS: data[constants.USER__EMAIL_ADDRESS]
            })
            if user:
                if user.verify_password(password=data[constants.USER__PASSWORD]):
                    expiry_time = config.TOKEN_EXPIRY_TIME_WEB
                    token_is_valid, token_error_messages, token = TokenController.generate_access_token(
                        user=user, purpose=constants.PURPOSE_LOGIN,
                        expiry_time=expiry_time)
                    if token_is_valid:
                        return response_utils.get_response_object(
                            response_code=response_codes.CODE_SUCCESS,
                            response_message=response_codes.MESSAGE_LOGIN_SUCCESS,
                            response_data=token.display())

                    else:
                        return response_utils.get_response_object(
                            response_code=response_codes.CODE_VALIDATION_FAILED,
                            response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                            response_data=token_error_messages
                        )
                else:
                    return response_utils.get_response_object(
                        response_code=response_codes.CODE_INVALID_PASSWORD,
                        response_message=response_codes.MESSAGE_INVALID_DATA.format(
                            constants.USER__PASSWORD
                        ))
            else:
                return response_utils.get_response_object(
                    response_code=response_codes.CODE_INVALID_EMAIL_ADDRESS,
                    response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                        constants.USER.title(), constants.USER__EMAIL_ADDRESS
                    ))
        else:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )

    @classmethod
    def logout_controller(cls):
        logged_in_user = common_utils.current_user()
        TokenController.suspend_user_tokens(
            read_filter={constants.TOKEN__USER: logged_in_user})
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS, response_message=response_codes.MESSAGE_LOGOUT_SUCCESS
        )

    @classmethod
    def get_user_childs(cls, user, search_depth=4, return_self=True):
        user_level__dict = {
            constants.ADMIN: 4,
            constants.GM: 3,
            constants.DGM: 2,
            constants.AM: 1,
            constants.AGENT: 0,
            constants.DGM_AGENT: 0,
            constants.DGM_LANCER: 0,
            constants.AM_LANCER: 0
        }
        user_level = user_level__dict[user[constants.USER__ROLE]
                                      [constants.USER__ROLE__NAME]]
        if user_level > search_depth:
            user_level = search_depth
        if user_level == 4:
            return cls.db_read_records(read_filter={})
        user__childs_list = [cls.db_read_records(
            read_filter={constants.USER__MANAGER: user})]
        for _ in range(user_level-1):
            current_level_childs = cls.db_read_records(read_filter={
                constants.USER__MANAGER+"__in": user__childs_list[0]})
            user__childs_list.insert(0, current_level_childs)
        user__childs = []
        for list_childs in user__childs_list:
            user__childs.extend(list_childs)
        if return_self:
            user__childs.append(user)
        return user__childs

    @classmethod
    def get_user(cls, data):
        return cls.db_read_single_record(read_filter={constants.ID: data}, deleted_records=True)

    @classmethod
    def get_users_childs_list(cls, data):
        user_childs = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        child_list = [user.display() for user in user_childs]
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_LOGIN_SUCCESS,
            response_data=child_list)
