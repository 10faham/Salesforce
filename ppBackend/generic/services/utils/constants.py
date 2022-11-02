# Python imports
import json

# Local imports
from ppBackend import config


# Reading Static Data
static_data = {}
with open(config.static_data_path, "r") as static_data_file:
    static_data = json.load(static_data_file)

# Validation Response Messages
VALIDATION_MESSAGES = {
    "REQUIRED": "{} is required",
    "NONEXISTENT": "{} should not be provided",
    "UNIQUE": "{} has to be unique",
    "EXISTS": "{} with this {} does not exist",
    "PASSWORD": {
        "MINIMUM_LENGTH_ERROR": "{} must contain minimum 8 characters",
        "MISSING_LOWERCASE": "{} must contain a single LowerCase character",
        "MISSING_UPPERCASE": "{} must contain a single UpperCase character",
        "MISSING_NUMBER": "{} must contain a single Number",
        "MISSING_SPECIAL": "{} must contain a single Special character",
    },
    "UID": "Please Enter a Valid {}",
    "EMAIL": "Please Enter a Valid {}",
    "PHONE_NUMBER": "Please Enter a Valid {}",
    "DATATYPE": "The Field {} has to be a type of {}",
    "DATETIME_FORMAT": "The Field {} should be in valid Date Time Format i.e "
    + config.DATETIME_FORMAT,
    "DATE_FORMAT": "The Field {} has to contain a valid Date Format i.e "
    + config.DATE_FORMAT,
    "CHOICES": "The Field {} has to be a value in {}",
    "LENGTH": "The Field {} has to be of length {}",
    "MAX_LENGTH": "The Length of Field {} has to be less than {}",
    "MIN_LENGTH": "The Length of Field {} has to be greater than {}",
    "FORMAT": "The Format of Field {} is incorrect Errors : {}",
}

# Validation constants
GENDER_LIST = static_data["gender"]
# Default Validation of Data before it is inserted into the database
DEFAULT_VALIDATION = True
# Default if to read is_deleted = True records from database
DEFAULT_READ_DELETED_RECORDS = False
# Update modes Database Layer
UPDATE_MODE__FULL = "full"
UPDATE_MODE__PARTIAL = "partial"

# DEFAULT OBJECTS
OBJECT_STATUS_ACTIVE = static_data["statuses"][0]
OBJECT_STATUS_INACTIVE = static_data["statuses"][1]
OBJECT_STATUS_SUSPENDED = static_data["statuses"][2]
# DEFAULT ROLES
DEFAULT_ADMIN_ROLE_OBJECT = static_data["user_roles_and_rights"][0]
DEFAULT_GM_ROLE_OBJECT = static_data["user_roles_and_rights"][1]
DEFAULT_DGM_ROLE_OBJECT = static_data["user_roles_and_rights"][2]
DEFAULT_AM_ROLE_OBJECT = static_data["user_roles_and_rights"][3]
DEFAULT_AGENT_ROLE_OBJECT = static_data["user_roles_and_rights"][4]
DEFAULT_DGM_AGENT_ROLE_OBJECT = static_data["user_roles_and_rights"][5]
DEFAULT_DEFAULT_ROLE_OBJECT = static_data["user_roles_and_rights"][6]
DEFAULT_ROLE_OBJECTS = [
    DEFAULT_ADMIN_ROLE_OBJECT,
    DEFAULT_GM_ROLE_OBJECT,
    DEFAULT_DGM_ROLE_OBJECT,
    DEFAULT_AM_ROLE_OBJECT,
    DEFAULT_AGENT_ROLE_OBJECT,
    DEFAULT_DGM_AGENT_ROLE_OBJECT,
]

OBJECT_STATUS_ACTIVE_ID = 1
OBJECT_STATUS_INACTIVE_ID = 2
OBJECT_STATUS_SUSPENDED_ID = 3


# STARTING
STATIC_DATA = static_data

SEARCH_DEPTH_MAX = 4

# USER TYPES
ADMIN = "admin"
GM = "gm"
DGM = "dgm"
AM = "am"
AGENT = "agent"
DGM_AGENT = "dgm_agent"
DGM_LANCER = "dgm_lancer"
AM_LANCER = "am_lancer"


# USER ROLE IDS
ROLE_ID_ADMIN = 1
ROLE_ID_GM = 2
ROLE_ID_DGM = 3
ROLE_ID_AM = 4
ROLE_ID_AGENT = 5
ROLE_ID_DGM_AGENT = 6
ROLE_ID_DGM_LANCER = 7
ROLE_ID_AM_LANCER = 8

# ENDING


ID = "id"
STATUS = "status"
STATUS__ID = "id"
STATUS__NAME = "name"
CREATED_ON = "created_on"
UPDATED_ON = "updated_on"
CREATED_BY = "created_by"
UPDATED_BY = "updated_by"


CURRENT_TIME = "current_time"

ADDRESS__COUNTRY = "country"
ADDRESS__PROVINCE = "province"
ADDRESS__CITY = "city"
ADDRESS__AREA = "area"
ADDRESS__STREET_ADDRESS = "street_address"

ADDRESS_VALIDATION_FORMAT = {
    "key": [
        {
            "rule": "choices",
            "options": [
                ADDRESS__COUNTRY,
                ADDRESS__PROVINCE,
                ADDRESS__CITY,
                ADDRESS__AREA,
                ADDRESS__STREET_ADDRESS,
            ],
        }
    ],
    "value": [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
}

FILTER__NEW = "new"
FILTER__OLD = "old"
FILTER_LIST = [FILTER__NEW, FILTER__OLD]

# USER LOGIN CHANNELS
EMAIL = "email"
PHONE = "phone"
LOGGED_IN_USER = "logged_in_user"
# PLATFORM_WEB = 'web'
# PLATFORM_MOBILE = 'mobile'
PURPOSE_LOGIN = "login-user"
PURPOSE_RESET_PASSWORD = "reset-password"

# Change Password Email
# PLATFORM_EMAIL = 'email'


# USER CONSTANTS
USER = "user"
USER__NAME = "name"
USER__EMAIL_ADDRESS = "email_address"
USER__PHONE_NUMBER = "phone_number"
USER__PASSWORD = "password"
USER__GENDER = "gender"
USER__NIC = "nic"
USER__ROLE = "role"
USER__MANAGER = "manager"
USER__ROLE__ROLE_ID = "user_role_id"
USER__ROLE__NAME = "name"
USER__ROLE__TITLE = "title"
USER__ROLE__RIGHTS = "rights"
USER__ROLE__MANAGER = "manager"
USER__ROLE__MANAGER_ID = "manager_id"
USER__ROLE__MANAGER_NAME = "manager_name"

USER__NEW_PASSWORD = "new_password"
USER__OLD_PASSWORD = "old_password"


# TOKEN Constants
TOKEN = "token"
TOKEN__ACCESS_TOKEN = "access_token"
TOKEN__USER = "user"
TOKEN__PURPOSE = "purpose"
TOKEN__EXPIRY_TIME = "expiry_time"
TOKEN__IS_EXPIRED = "is_expired"
TOKEN__IS_REVOKED = "is_revoked"

# Client Constants
CLIENT = "lead"
CLIENT__ID = "lead_id"
CLIENT__NAME = "first_name"
CLIENT__NIC = "nic"
CLIENT__PHONE_NUMBER = "phone_number"
CLIENT__EMAIL_ADDRESS = "email_address"
CLIENT__ADDRESS = "address"
CLIENT__ADDRESS__KEY_LIST = ["Home", "Office"]
CLIENT__GENDER = "gender"
CLIENT__COUNTRY = "country"
CLIENT__CITY = "city"
CLIENT__CLIENT_CATEGORY = "client_category"
CLIENT__CLIENT_CATEGORY__LIST = ["Investor", "User", "Agent"]
CLIENT__ASSIGNED_TO = "assigned_to"
CLIENT__ASSIGNED_BY = "assigned_by"
CLIENT__TRANSFERED = "transfered"
CLIENT__TRANSFERED_ON = "transfered_on"

# Lead Constants
LEAD = "lead"
LEAD__ID = "lead_id"
LEAD__FIRST_NAME = "first_name"
LEAD__LAST_NAME = "last_name"
LEAD__NIC = "nic"
LEAD__PHONE_NUMBER = "phone_number"
LEAD__LANDLINE_NUMBER = "landline_number"
LEAD__EMAIL_ADDRESS = "email_address"
LEAD__ADDRESS = "address"
LEAD__ADDRESS__KEY_LIST = ["Home", "Office"]
LEAD__PROJECT = "project"
LEAD__SOURCE = "lead_source"
LEAD__STATUS = "lead_status"
LEAD__STATUS__LIST = ["Interested", "Not Interested"]
LEAD__GENDER = "gender"
LEAD__COUNTRY = "country"
LEAD__CITY = "city"
LEAD__CLIENT_CATEGORY = "client_category"
LEAD__CLIENT_CATEGORY__LIST = ["Investor", "User", "Agent"]
LEAD__LEVEL = "lead_level"
LEAD__LEVEL__LIST = ["AtomBomb", "Hot", "Moderate", "Cold", "SubZero"]
LEAD__USER = "user"
LEAD__COMMENT = "lead_comment"
LEAD__ASSIGNED_TO = "assigned_to"
LEAD__ASSIGNED_BY = "assigned_by"
LEAD__TRANSFERED = "transfered"
LEAD__FOLLOWUP = "followup_id"
LEAD__LAST_WORK = "followup_last_work"
LEAD__LAST_WORK_DATE = "followup_last_work_date"
LEAD__FOLLOWUP_COUNT = "followup_count"
LEAD__FOLLOWUP_NEXT_DEADLINE = "next_deadline"
LEAD__FOLLOWUP_NEXT_TASK = "followup_next_task"
LEAD__FOLLOWUP_REF_ID = "followup_ref_id"
LEAD__FOLLOWUP_TYPE = "followup_type"
LEAD__TRANSFERED_ON = "transfered_on"

# Lead History Constants
LEAD_HISTORY = "lead_history"
HISTORY__ID = "history_id"
LEAD__ID = "lead_id"
LEAD_HISTORY__FIRST_NAME = "first_name"
LEAD_HISTORY__LAST_NAME = "last_name"
LEAD_HISTORY__NIC = "nic"
LEAD_HISTORY__PHONE_NUMBER = "phone_number"
LEAD_HISTORY__LANDLINE_NUMBER = "landline_number"
LEAD_HISTORY__EMAIL_ADDRESS = "email_address"
LEAD_HISTORY__ADDRESS = "address"
LEAD_HISTORY__ADDRESS__KEY_LIST = ["Home", "Office"]
LEAD_HISTORY__PROJECT = "project"
LEAD_HISTORY__SOURCE = "lead_source"
LEAD_HISTORY__STATUS = "lead_status"
LEAD_HISTORY__STATUS__LIST = ["Interested", "Not Interested"]
LEAD_HISTORY__GENDER = "gender"
LEAD_HISTORY__COUNTRY = "country"
LEAD_HISTORY__CITY = "city"
LEAD_HISTORY__CLIENT_CATEGORY = "client_category"
LEAD_HISTORY__CLIENT_CATEGORY__LIST = ["Investor", "User", "Agent"]
LEAD_HISTORY__LEVEL = "lead_level"
LEAD_HISTORY__LEVEL__LIST = ["AtomBomb", "Hot", "Moderate", "Cold", "SubZero"]
LEAD_HISTORY__USER = "user"
LEAD_HISTORY__COMMENT = "lead_comment"
LEAD_HISTORY__ASSIGNED_TO = "assigned_to"
LEAD_HISTORY__ASSIGNED_BY = "assigned_by"
LEAD_HISTORY__TRANSFERED = "transfered"
LEAD_HISTORY__FOLLOWUP = "followup_id"
LEAD_HISTORY__TRANSFERED_ON = "transfered_on"

# Follow Up Constants
FOLLOW_UP = "follow_up"
FOLLOWUP__ID = "follow_id"
FOLLOW_UP__LEAD = "lead"
FOLLOW_UP__TYPE = "type"
FOLLOW_UP__TYPE_LIST = ["Call", "Meeting"]
FOLLOW_UP__SUB_TYPE = "sub_type"
FOLLOW_UP__LEVEL = "lead_level"
FOLLOW_UP__LEVEL__LIST = ["AtomBomb", "Hot", "Moderate", "Cold", "SubZero"]
FOLLOW_UP__STATUS = "lead_status"
FOLLOW_UP__STATUS__LIST = ["Interested", "Not Interested"]
FOLLOW_UP__COMPLETION_DATE = "completion_date"
FOLLOW_UP__COMMENT = "comment"
FOLLOW_UP__ASSIGNED_TO = "assigned_to"

FOLLOW_UP__NEXT_TASK = "next_task"
FOLLOW_UP__NEXT_PROJECT = "next_project"
FOLLOW_UP__NEXT_DEADLINE = "next_deadline"
FOLLOW_UP__NEXT_COMMENT = "next_comment"
DATE_FROM = "date_start"
DATE_TO = "date_end"

# Required, Optional Fields Lists
# User
LOGIN_REQUIRED_FIELDS_LIST = [USER__EMAIL_ADDRESS, USER__PASSWORD]
REQUIRED_FIELDS_LIST__USER = [
    USER__NAME,
    USER__EMAIL_ADDRESS,
    USER__PASSWORD,
    USER__PHONE_NUMBER,
    USER__GENDER,
    USER__ROLE,
    USER__NIC
]
OPTIONAL_FIELDS_LIST__USER = [
    USER__EMAIL_ADDRESS,
    USER__PHONE_NUMBER,
    # USER__ROLE__MANAGER_NAME,
    USER__MANAGER]
REQUIRED_UPDATE_FIELDS_LIST__USER = list(
    set(REQUIRED_FIELDS_LIST__USER + [ID])
    - set([USER__PASSWORD, USER__EMAIL_ADDRESS, USER__PHONE_NUMBER])
)
ALL_FIELDS_LIST__USER = OPTIONAL_FIELDS_LIST__USER + \
    REQUIRED_FIELDS_LIST__USER + [ID]

# Lead
REQUIRED_FIELDS_LIST__LEAD = [
    LEAD__FIRST_NAME,
    LEAD__GENDER,
    LEAD__COUNTRY,
    LEAD__CITY,
    LEAD__PHONE_NUMBER,
    LEAD__LEVEL
]
OPTIONAL_FIELDS_LIST__LEAD = [
    LEAD__LAST_NAME,
    LEAD__NIC,
    LEAD__LANDLINE_NUMBER,
    LEAD__EMAIL_ADDRESS,
    LEAD__ADDRESS,
    LEAD__PROJECT,
    LEAD__SOURCE,
    LEAD__GENDER,
    LEAD__CLIENT_CATEGORY,
    LEAD__COMMENT
]
REQUIRED_UPDATE_FIELDS_LIST__LEAD = list(
    set([ID])
)
ALL_FIELDS_LIST__LEAD = OPTIONAL_FIELDS_LIST__LEAD + \
    REQUIRED_FIELDS_LIST__LEAD + [ID, CREATED_BY, CREATED_ON]

# Follow Up
REQUIRED_FIELDS_LIST__FOLLOW_UP = [
    FOLLOW_UP__LEAD,
    FOLLOW_UP__TYPE,
    FOLLOW_UP__SUB_TYPE,
    FOLLOW_UP__LEVEL,
    FOLLOW_UP__COMMENT,
    FOLLOW_UP__NEXT_TASK,
    FOLLOW_UP__NEXT_DEADLINE,
]
OPTIONAL_FIELDS_LIST__FOLLOW_UP = [
    FOLLOW_UP__COMPLETION_DATE,
    FOLLOW_UP__NEXT_COMMENT,
    FOLLOW_UP__NEXT_PROJECT

]
REQUIRED_UPDATE_FIELDS_LIST__FOLLOW_UP = list(
    set(REQUIRED_FIELDS_LIST__FOLLOW_UP + [ID]) - set([LEAD__FIRST_NAME])
)
ALL_FIELDS_LIST__FOLLOW_UP = OPTIONAL_FIELDS_LIST__FOLLOW_UP + \
    REQUIRED_FIELDS_LIST__FOLLOW_UP + [ID, CREATED_BY]

REQUIRED_FIELDS_LIST__FOLLOW_UP_LEAD = [
    FOLLOW_UP__LEAD
]

#Add leads + follow_ups

REQUIRED_FIELDS_LIST__LEAD_FOLLOWUP = [
    LEAD__FIRST_NAME,
    LEAD__GENDER,
    LEAD__COUNTRY,
    LEAD__CITY,
    LEAD__LEVEL,
    FOLLOW_UP__TYPE,
    FOLLOW_UP__SUB_TYPE,
    FOLLOW_UP__LEVEL,
    FOLLOW_UP__COMMENT,
    LEAD__PHONE_NUMBER,
    FOLLOW_UP__NEXT_TASK
]
OPTIONAL_FIELDS_LIST__LEAD_FOLLOWUP = [
    LEAD__LAST_NAME,
    LEAD__NIC,
    LEAD__LANDLINE_NUMBER,
    LEAD__EMAIL_ADDRESS,
    LEAD__ADDRESS,
    LEAD__PROJECT,
    LEAD__SOURCE,
    LEAD__GENDER,
    LEAD__CLIENT_CATEGORY,
    LEAD__COMMENT,
    FOLLOW_UP__COMPLETION_DATE,
    FOLLOW_UP__NEXT_DEADLINE,
    FOLLOW_UP__NEXT_COMMENT,
    FOLLOW_UP__NEXT_PROJECT
]

#Clients 

REQUIRED_FIELDS_LIST__CLIENTS = [
    CLIENT__NAME,
    CLIENT__NIC,
    CLIENT__PHONE_NUMBER,
    CLIENT__EMAIL_ADDRESS,
    CLIENT__ADDRESS,
    CLIENT__GENDER,
    CLIENT__COUNTRY,
    CLIENT__CITY,
    CLIENT__CLIENT_CATEGORY,
]

#temp fields

PROJECT = [
    'Anabia Residency',
    'Crown Residency',
    'Tricon',
    'MZN Tower',
    'MZN Villas',
    'Gul Mohar'
]