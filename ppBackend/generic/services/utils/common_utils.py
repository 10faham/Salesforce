# Python imports
import datetime
import time
import re
import json
import uuid
# Local imports
from ppBackend.generic.services.utils import constants, __global__
from ppBackend.config import config

# Framework imports
from flask import request, abort


def posted():
    """
    Get Data
    :return:
    """
    if request.method == "GET":
        return request.args or {}
    return request.get_json(silent=True) or {}


def posted_files():
    """
    Get Data
    :return:
    """
    return request.files or {}


def posted_form_data():
    """
    Get Data
    :return:
    """
    return request.form or {}


def raise_response_code(code):
    abort(code)


def get_time(offset=0, days=0):
    """ return serialized datetime current + offset in hours """
    hours = offset
    return int(time.mktime(
        (datetime.datetime.now() +
         datetime.timedelta(hours=hours, days=days)).timetuple())
        * 1000)


def format_datetime(str_datetime, format=config.DATETIME_FORMAT):
    try:
        return datetime.datetime.strptime(str(str_datetime), format)
    except ValueError:
        return None


def format_date(str_date, format=config.DATE_FORMAT):
    try:
        return datetime.datetime.strptime(str(str_date), format)
    except ValueError:
        return None


def convert_to_epoch(str_time, format=config.DATETIME_FORMAT):
    return int(time.mktime(time.strptime(str_time, format)))


def json_to_dict(json_data):
    return json.loads(json_data)


def generate_uuid4():
    return str(uuid.uuid4())


def validate_password(password):
    if len(password) < 8:
        return [
            False,
            constants.VALIDATION_MESSAGES["PASSWORD"]["MINIMUM_LENGTH_ERROR"]]
    if not re.match('.*[a-z].*', password):
        return [False,
                constants.VALIDATION_MESSAGES["PASSWORD"]["MISSING_LOWERCASE"]]

    if not re.match('.*[A-Z].*', password):
        return [False,
                constants.VALIDATION_MESSAGES["PASSWORD"]["MISSING_UPPERCASE"]]

    if not re.match('.*[0-9].*', password):
        return [False,
                constants.VALIDATION_MESSAGES["PASSWORD"]["MISSING_NUMBER"]]

    if not re.match('.*[.~`!@#$%^&*(){};:/?<>,|*-+].*', password):
        return [False,
                constants.VALIDATION_MESSAGES["PASSWORD"]["MISSING_SPECIAL"]]

    return True, ""


def encrypt_password(password):
    """ return Encrypted Password  """
    from ppBackend import bcrypt
    return bcrypt.generate_password_hash(password).decode('utf-8')


def verify_password(password_hash, password):
    """ return if the password_hash matches the hash or :param: password """
    from ppBackend import bcrypt
    return bcrypt.check_password_hash(password_hash, password)


def get_access_token():
    """ Gets user token from header. """
    return request.cookies.get('access_token', None)


def get_token():
    access_token = get_access_token()
    if not access_token:
        return None
    from ppBackend.UserManagement.controllers.TokenController import TokenController
    token_obj = TokenController.authenticate_token(access_token, purpose=constants.PURPOSE_LOGIN)
    if not token_obj:
        return None
    user = token_obj[constants.USER].fetch()
    __global__.set_current_user(user)
    return token_obj


def current_user():
    user = __global__.get_current_user()
    if user:
        return user
    token_obj = get_token()
    if token_obj:
        return token_obj[constants.TOKEN__USER].fetch()
    print('User not found')
    return None
