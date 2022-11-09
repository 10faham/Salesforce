# Python imports

# Framework imports

# Local imports
from ppBackend.generic import models
from ppBackend.generic import db
from ppBackend.generic.services.utils import constants, common_utils
from ppBackend.UserManagement.models.User import User
# from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController



class LeadHistory(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.LEAD_HISTORY__FIRST_NAME: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__LAST_NAME: [{"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__NIC: [{"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__LANDLINE_NUMBER: [{"rule": "phone_number"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__EMAIL_ADDRESS: [{"rule": "email"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__ADDRESS: [{"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__PROJECT: [{"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__SOURCE: [{"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__STATUS: [{"rule": "choices", "options": constants.LEAD_HISTORY__STATUS__LIST}],
            constants.LEAD_HISTORY__GENDER: [{"rule": "choices", "options": constants.GENDER_LIST}],
            constants.LEAD_HISTORY__COUNTRY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__CITY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__COMMENT: [{"rule": "datatype", "datatype": str}],
            constants.LEAD_HISTORY__CLIENT_CATEGORY: [{"rule": "choices", "options": constants.LEAD_HISTORY__CLIENT_CATEGORY__LIST}],
            constants.LEAD_HISTORY__LEVEL: [{"rule": "required"}, {"rule": "choices", "options": constants.LEAD_HISTORY__LEVEL__LIST}],

        }

    @classmethod
    def update_validation_rules(cls): return {
        constants.LEAD_HISTORY__FIRST_NAME: [{"rule": "nonexistent"}],
        constants.LEAD_HISTORY__STATUS: [{"rule": "nonexistent"}],
        constants.LEAD_HISTORY__GENDER: [{"rule": "nonexistent"}],
        constants.LEAD_HISTORY__COUNTRY: [{"rule": "nonexistent"}],
        constants.LEAD_HISTORY__CITY: [{"rule": "nonexistent"}],
        constants.LEAD_HISTORY__LEVEL: [{"rule": "nonexistent"}]
    }

    first_name = db.StringField(required=True)
    last_name = db.StringField()
    nic = db.StringField()
    phone_number = db.ListField()
    landline_number = db.StringField()
    email_address = db.StringField()
    address = db.StringField()
    project = db.StringField()
    lead_source = db.StringField()
    lead_status = db.StringField()
    gender = db.StringField()
    country = db.StringField(required=True)
    city = db.StringField(required=True)
    client_category = db.StringField()
    lead_level = db.StringField(required=True)
    lead_comment = db.StringField()
    assigned_to = db.LazyReferenceField(User, required=True)
    assigned_by = db.LazyReferenceField(User, required=True)
    history_id = db.SequenceField(value_decorator='LH-{}'.format)
    lead_id = db.StringField()
    transfered = db.BooleanField(default=False)
    transfered_on = db.IntField()

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.HISTORY__ID: self[constants.HISTORY__ID],
            constants.LEAD_HISTORY__FIRST_NAME: self[constants.LEAD_HISTORY__FIRST_NAME],
            constants.LEAD_HISTORY__LAST_NAME: self[constants.LEAD_HISTORY__LAST_NAME],
            constants.LEAD_HISTORY__NIC: self[constants.LEAD_HISTORY__NIC],
            constants.LEAD_HISTORY__PHONE_NUMBER: self[constants.LEAD_HISTORY__PHONE_NUMBER],
            constants.LEAD_HISTORY__LANDLINE_NUMBER: self[constants.LEAD_HISTORY__LANDLINE_NUMBER],
            constants.LEAD_HISTORY__EMAIL_ADDRESS: self[constants.LEAD_HISTORY__EMAIL_ADDRESS],
            constants.LEAD_HISTORY__ADDRESS: self[constants.LEAD_HISTORY__ADDRESS],
            constants.LEAD_HISTORY__PROJECT: self[constants.LEAD_HISTORY__PROJECT],
            constants.LEAD_HISTORY__SOURCE: self[constants.LEAD_HISTORY__SOURCE],
            constants.LEAD_HISTORY__STATUS: self[constants.LEAD_HISTORY__STATUS],
            constants.LEAD_HISTORY__GENDER: self[constants.LEAD_HISTORY__GENDER],
            constants.LEAD_HISTORY__COUNTRY: self[constants.LEAD_HISTORY__COUNTRY],
            constants.LEAD_HISTORY__CITY: self[constants.LEAD_HISTORY__CITY],
            constants.LEAD_HISTORY__CLIENT_CATEGORY: self[constants.LEAD_HISTORY__CLIENT_CATEGORY],
            constants.LEAD_HISTORY__LEVEL: self[constants.LEAD_HISTORY__LEVEL],
            constants.LEAD_HISTORY__COMMENT: self[constants.LEAD_HISTORY__COMMENT],
            constants.LEAD_HISTORY__ASSIGNED_TO: self[constants.LEAD_HISTORY__ASSIGNED_TO].fetch().name if self[constants.LEAD_HISTORY__ASSIGNED_TO] else None,
            constants.LEAD_HISTORY__ASSIGNED_BY: self[constants.LEAD_HISTORY__ASSIGNED_BY].fetch().name if self[constants.LEAD_HISTORY__ASSIGNED_BY] else None,
            constants.LEAD_HISTORY__TRANSFERED: self[constants.LEAD_HISTORY__TRANSFERED] if self[constants.LEAD_HISTORY__TRANSFERED] else False,
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self.created_by.fetch().name,
            constants.CREATED_ON: common_utils.epoch_to_datetime(self[constants.CREATED_ON]),
            constants.UPDATED_ON: common_utils.epoch_to_datetime(self[constants.UPDATED_ON])
        }

    def display_min(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.LEAD__ID: self[constants.LEAD__ID],
            constants.LEAD_HISTORY__FIRST_NAME: self[constants.LEAD_HISTORY__FIRST_NAME],
            constants.LEAD_HISTORY__PHONE_NUMBER: self[constants.LEAD_HISTORY__PHONE_NUMBER],
            constants.LEAD_HISTORY__PROJECT: self[constants.LEAD_HISTORY__PROJECT],
            constants.LEAD_HISTORY__LEVEL: self[constants.LEAD_HISTORY__LEVEL],
            constants.LEAD_HISTORY__ASSIGNED_TO: self[constants.LEAD_HISTORY__ASSIGNED_TO].fetch().name,
            constants.CREATED_ON: common_utils.epoch_to_datetime(self[constants.CREATED_ON]),
        }