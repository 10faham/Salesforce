# Python imports
import re

from flask_mongoengine import BaseQuerySet
# Local imports
from ppBackend.generic.services.utils import common_utils, constants
from ppBackend.config import config

# TODO Add Rules : URL


def validate_data(data, validation_rules={}):
    """
        Validate data with respect to validation_rules and operation type
        :param data: Dict obj of data to be validated
        :param validation_rules: Dict obj of validation rules to be run on data
        is creating new record else if it is False then operation is
        updating existing record
        :return:
        """
    if type(data) is str:
        data = common_utils.json_to_dict(data)
    error_list = []
    for key in validation_rules:
        if validation_rules[key]:
            rules = validation_rules[key]
            error_list.extend(validate_single_data(data, key, rules))
    return not (len(error_list) > 0), error_list


def validate_single_data(data, key, rules):
    error_list = []
    # Setting Default False as that we dont know for sure
    # if the data.get(key) is not None
    is_data_key_none = False
    if not data.get(key):
        is_data_key_none = True
    for rule in rules:
        function = rule["rule"]

        # Rules which dont require the data to be non None i.e.
        #  Rules which will work on None Data
        # TODO Create Rules which accept Nullable data
        # for e.g. Max_length, etc
        if function == "nonexistent":
            func_return = nonexistent(data, key)
            if not func_return[0]:
                error_list.append({key: func_return[1]})
        if function == "max_length":
            func_return = max_length(data, key, rule)
            if not func_return[0]:
                error_list.append({key: func_return[1]})
        # Checking if data is none or rule is required so then
        # we can check data to be validated
        if function == "required":
            func_return = required(data, key)
            if not func_return[0]:
                error_list.append({key: func_return[1]})
                break
        # TODO Create more Rules
        # Rules which require the data to be not None
        if not is_data_key_none:
            if function == "unique":
                func_return = unique(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "exists":
                func_return = exists(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "password":
                func_return = password(data, key)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "email":
                func_return = email(data, key)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "uid":
                func_return = uid(data, key)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "phone_number":
                func_return = phone_number(data, key)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "datatype":
                func_return = datatype(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "datetime_format":
                func_return = datetime_format(data, key)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "date_format":
                func_return = date_format(data, key)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "choices":
                func_return = choices(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "length":
                func_return = length(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "min_length":
                func_return = min_length(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
            if function == "collection_format":
                func_return = collection_format(data, key, rule)
                if not func_return[0]:
                    error_list.append({key: func_return[1]})
    return error_list


def required(data, key):
    if data.get(key) not in [None, ""]:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["REQUIRED"]
                .format(key.title())]


def nonexistent(data, key):
    if data.get(key) in [None, ""]:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["NONEXISTENT"]
                .format(key.title())]


def unique(data, key, rule):
    model = rule["Model"]
    field = rule["Field"]
    obj = None
    if(type(model) != BaseQuerySet):
        obj = model.objects(**{field: data[key]}).first()
    else:
        obj = model.filter(**{field: data[key]}).first()
    if (obj is None):
        return [True, ""]
    else:
        if data.get(constants.ID):
            if data[constants.ID] == obj[constants.ID]:
                return [True, ""]
        return [False, constants.VALIDATION_MESSAGES["UNIQUE"].format(field.title())]


def exists(data, key, rule):
    model = rule["Model"]
    field = rule["Field"]
    obj = None
    if(type(model) != BaseQuerySet):
        obj = model.objects(**{field: data[key]}).first()
    else:
        obj = model.filter(**{field: data[key]}).first()
        model = model._document
    if (obj):
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["EXISTS"]
                .format(model.__name__, field.title())]


def password(data, key):
    validation = common_utils.validate_password(data[key])
    if not validation[0]:
        validation[1] = validation[1].format(key.title())
    return validation


def email(data, key):
    email_regex = re.compile(
        r'^(?![.%+-])[a-zA-Z0-9._%+-]+[a-zA-Z0-9]+@[a-zA-Z0-9]+[+-]{0,1}[a-zA-Z0-9]+\.[a-zA-Z]+\.{0,1}[a-zA-Z]+$')
    if email_regex.match(str(data[key])):
        return [True, ""]
    else:
        return [False,
                constants.VALIDATION_MESSAGES["EMAIL"].format(key.title())]


def uid(data, key):
    uid_regex = r"^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$"
    if re.search(uid_regex, data[key], re.IGNORECASE):
        return [True, ""]
    else:
        return [False,
                constants.VALIDATION_MESSAGES["UID"].format(key.title())]


def phone_number(data, key):
    phone_number_regex = re.compile(r'^\+(?:[0-9]●?){6,14}[0-9]$')
    if phone_number_regex.match(str(data[key])):
        return [True, ""]
    else:
        return [False,constants.VALIDATION_MESSAGES["PHONE_NUMBER"].format(
                    key.title())]


def datatype(data, key, rule):
    required_datatype = rule["datatype"]
    if type(data[key]) is required_datatype:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["DATATYPE"]
                .format(str(key).title(), required_datatype)]


def datetime_format(data, key):
    if common_utils.format_datetime(data[key]):
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["DATETIME_FORMAT"]
                .format(key.title())]


def date_format(data, key):
    if common_utils.format_date(data[key]):
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["DATE_FORMAT"].format(
            key.title())]


def choices(data, key, rule):
    parameter_list = rule["options"]
    if data[key] in parameter_list:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["CHOICES"]
                .format(key.title(), parameter_list)]


def length(data, key, rule):
    required_length = rule["length"]
    if len(data[key]) == required_length:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["LENGTH"].format(
            key.title(), required_length)]


def max_length(data, key, rule):
    required_max_length = rule["length"]
    key_length = 0
    if data.get(key):
        key_length = len(data[key])
    if key_length <= required_max_length:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["MAX_LENGTH"].format(
            key.title(), required_max_length)]


def min_length(data, key, rule):
    required_min_length = rule["length"]
    if len(data[key]) >= required_min_length:
        return [True, ""]
    else:
        return [False, constants.VALIDATION_MESSAGES["MIN_LENGTH"].format(
            key.title(), required_min_length)]


def collection_format(data, key, rule):
    data_datetype = rule["datatype"]
    validation_rules = rule["validation_rules"]
    if data_datetype == dict:
        first_key = validation_rules["key"]
        first_value = validation_rules["value"]
        elements = data[key]
        error_messages_key = []
        error_messages_value = []
        for count, element_key in enumerate(elements):
            error_message_key = validate_single_data(
                {element_key: element_key}, element_key, first_key)
            error_message_value = validate_single_data(
                elements, element_key, first_value)
            if len(error_message_key) > 0:
                error_messages_key.append(
                    {"Index": count, "Error": error_message_key})
            if len(error_message_value) > 0:
                error_messages_value.append(
                    {"Index": count, "Error": error_message_value})
        if not (len(error_messages_key) > 0) and not (len(error_messages_value
                                                          ) > 0):
            return [True, ""]
        else:
            return [False, {
                "key": error_messages_key,
                "value": error_messages_value,
            }]
    elif data_datetype == list:
        validation_rules = rule["validation_rules"]
        error_messages = []
        for count, element in enumerate(data[key]):
            error_message = validate_single_data(
                {key: element}, key, validation_rules)
            if len(error_message) > 0:
                error_messages.append(
                    {"Index": count, "Error": error_message})
        if not (len(error_messages) > 0):
            return [True, ""]
        else:
            return [False, error_messages]
