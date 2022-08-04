# Python imports

# Framework imports

# Local imports
from ppBackend.generic import models
from ppBackend.generic import db
from ppBackend.generic.services.utils import constants, common_utils
from ppBackend.UserManagement.models.User import User

class Clients(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.CLIENT__NAME: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__NIC: [{"rule": "datatype", "datatype": str}],
            constants.CLIENT__PHONE_NUMBER:  [{"rule": "datatype", "datatype": list},
                                                {"rule": "collection_format", "datatype": list,
                                            "validation_rules": [{"rule": "required"}, {"rule": "phone_number"}]}],
            constants.CLIENT__EMAIL_ADDRESS: [{"rule": "email"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__ADDRESS: [{"rule": "datatype", "datatype": str}],
            constants.CLIENT__GENDER: [{"rule": "choices", "options": constants.GENDER_LIST}],
            constants.CLIENT__COUNTRY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__CITY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__CLIENT_CATEGORY: "client_category",
            constants.CLIENT__CLIENT_CATEGORY__LIST: ["Investor", "User", "Agent"],
        }

    @classmethod
    def update_validation_rules(cls): return {

    }

    name = db.StringField(required=True)
    nic = db.StringField()
    phone_number = db.ListField()
    email_address = db.StringField()
    address = db.DictField(db.StringField())
    gender = db.StringField()
    country = db.StringField(required=True)
    city = db.StringField(required=True)
    assigned_to = db.LazyReferenceField(User, required=True)
    assigned_by = db.LazyReferenceField(User, required=True)
    client_id = db.SequenceField(value_decorator='CL-{}'.format)
    transfered = db.BooleanField(default=False)
    transfered_on = db.IntField()

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.CLIENT__ID: self[constants.CLIENT__ID],
            constants.CLIENT__NAME: self[constants.CLIENT__NAME],
            constants.CLIENT__NIC: self[constants.CLIENT__NIC],
            constants.CLIENT__PHONE_NUMBER: self[constants.CLIENT__PHONE_NUMBER],
            constants.CLIENT__EMAIL_ADDRESS: self[constants.CLIENT__EMAIL_ADDRESS],
            constants.CLIENT__ADDRESS: self[constants.CLIENT__ADDRESS],
            constants.CLIENT__GENDER: self[constants.CLIENT__GENDER],
            constants.CLIENT__COUNTRY: self[constants.CLIENT__COUNTRY],
            constants.CLIENT__CITY: self[constants.CLIENT__CITY],
            constants.CLIENT__CLIENT_CATEGORY: self[constants.CLIENT__CLIENT_CATEGORY],
            constants.CLIENT__ASSIGNED_TO: self[constants.CLIENT__ASSIGNED_TO].fetch().name,
            constants.CLIENT__ASSIGNED_BY: self[constants.CLIENT__ASSIGNED_BY].fetch().name,
            constants.CLIENT__TRANSFERED: self[constants.CLIENT__TRANSFERED] if self[constants.CLIENT__TRANSFERED] else False,
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self.created_by.fetch().name,
            constants.CREATED_ON: self[constants.CREATED_ON],
            constants.UPDATED_ON: self[constants.UPDATED_ON],
            constants.CLIENT__TRANSFERED_ON: self[constants.CLIENT__TRANSFERED_ON] if self[constants.CLIENT__TRANSFERED_ON] else False
        }

    def display_min(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.CLIENT__ID: self[constants.CLIENT__ID],
            constants.CLIENT__NAME: self[constants.CLIENT__NAME],
            constants.CLIENT__PHONE_NUMBER: self[constants.CLIENT__PHONE_NUMBER],
            constants.CLIENT__ASSIGNED_TO: self[constants.CLIENT__ASSIGNED_TO].fetch().name,
            constants.CREATED_ON: common_utils.epoch_to_datetime(self[constants.CREATED_ON]),
        }