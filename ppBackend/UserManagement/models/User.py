# Python imports

# Framework imports

# Local imports
from ppBackend.generic import models
from ppBackend.generic import db
from ppBackend.generic.services.utils import common_utils, constants


class User(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.USER__NAME: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
            ],
            constants.USER__EMAIL_ADDRESS: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
                {
                    "rule": "unique",
                    "Model": cls,
                    "Field": constants.USER__EMAIL_ADDRESS,
                },
            ],
            constants.USER__PHONE_NUMBER: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
                {
                    "rule": "unique",
                    "Model": cls,
                    "Field": constants.USER__PHONE_NUMBER,
                },
            ],
            constants.USER__PASSWORD: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
                {"rule": "password"},
            ],
            constants.USER__GENDER: [
                {"rule": "required"},
                {"rule": "choices", "options": constants.GENDER_LIST},
            ],
            constants.USER__NIC: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
                {
                    "rule": "unique",
                    "Model": cls,
                    "Field": constants.USER__NIC,
                },
            ],
            constants.USER__ROLE: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": dict},
                {"rule": "choices", "options": constants.DEFAULT_ROLE_OBJECTS},
            ],
            constants.USER__MANAGER: [],
        }

    @classmethod
    def login_validation_rules(cls):
        return {
            constants.USER__EMAIL_ADDRESS: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
            ],
            constants.USER__PASSWORD: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str},
                {"rule": "password"},
            ],
        }

    @classmethod
    def update_validation_rules(cls):
        return {}

    name = db.StringField(required=True)
    email_address = db.StringField(required=True)
    phone_number = db.StringField(required=True)
    password = db.StringField(required=True)
    gender = db.StringField(required=True)
    nic = db.StringField(required=True)
    role = db.DictField(required=True)
    manager = db.LazyReferenceField('User')
    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.USER__NAME: self[constants.USER__NAME],
            constants.USER__EMAIL_ADDRESS: self[constants.USER__EMAIL_ADDRESS],
            constants.USER__PHONE_NUMBER: self[constants.USER__PHONE_NUMBER],
            constants.USER__GENDER: self[constants.USER__GENDER],
            constants.USER__NIC: self[constants.USER__NIC],
            constants.USER__ROLE: self[constants.USER__ROLE],
            constants.STATUS: self[constants.STATUS],
        }

    def verify_password(self, password):
        return common_utils.verify_password(self.password, password)
