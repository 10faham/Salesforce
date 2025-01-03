# Python imports
import os
# Local imports


# ENVIRONMENT = "LOCAL"
ENVIRONMENT = "STAGING"

FUNCTION_LOGGING = False

current_dir_path = os.path.dirname(os.path.abspath(__file__))
static_data_path = os.path.join(current_dir_path, "static//static_data.json")
upload_files_path = os.path.join(os.getcwd(), "//uploads")


#  EXPIRY TIME IN HOURS
TOKEN_EXPIRY_TIME_WEB = 2
# TOKEN_EXPIRY_TIME_MOBILE = False
# TOKEN_EXPIRY_TIME_EMAIL = 0.5

FIREBASE_CONFIG = {}

FCM_API_KEY = ""


# Order VAT Rate i.e 1.15 = 15%
VAT_RATE = 1.15
# Newly Launched Filter Data Days
FILTER__NEW__TIME_DAYS = -30

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d-%m-%Y"
DISPLAY_TIME_FORMAT = "%H:%M:%S"
FILTER_DATE_FORMAT = "%d %m %Y"
FILTER_DATETIME_FORMAT = "%d %m %Y %H:%M:%S"
TIME_ZONE = "Asia/Karachi"

FRONTEND_URL = "https://proppioneers.com"
MONGO_DB_USER = ""
MONGO_DB_PASSWORD = ""

MONGO_DB_URI = ""
if ENVIRONMENT == "LOCAL":
    MONGO_DB_URI = f"mongodb+srv://faham:PNYpOYDAb4MsnfMn@cluster0.tncuc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
if ENVIRONMENT == "STAGING":
    FUNCTION_LOGGING = True
    static_data_path = os.path.join(
        current_dir_path, "static/static_data.json")
    upload_files_path = os.path.join(current_dir_path, "static/uploads")
    MONGO_DB_URI = f"mongodb+srv://faham:PNYpOYDAb4MsnfMn@cluster0.tncuc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # MONGO_DB_URI = f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@clusterX.aq4vs.mongodb.net/ppbackend?"\
    #     "retryWrites=true&w=majority"

DEFAULT_ADMIN_NAME = "Admin"
DEFAULT_ADMIN_EMAIL = "admin@mail.com"
DEFAULT_ADMIN_PASSWORD = "Admin@123"
DEFAULT_ADMIN_PHONE = "+9233121212"

# EMAIL_USER = "ppBackend316@gmail.com"
# EMAIL_PASSWORD = "ppbackend123"

MAIL_SETTINGS = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "admin@mail.com",
    "MAIL_PASSWORD": "Admin@123"
}
