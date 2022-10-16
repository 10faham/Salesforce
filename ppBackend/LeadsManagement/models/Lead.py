# Python imports

# Framework imports

# Local imports
from ppBackend.generic import models
from ppBackend.generic import db
from ppBackend.generic.services.utils import constants, common_utils
from ppBackend.UserManagement.models.User import User

class Leads(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.LEAD__FIRST_NAME: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD__LAST_NAME: [{"rule": "datatype", "datatype": str}],
            constants.LEAD__NIC: [{"rule": "datatype", "datatype": str}],
            # constants.LEAD__PHONE_NUMBER: [{"rule": "phone_number"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD__LANDLINE_NUMBER: [{"rule": "phone_number"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD__PHONE_NUMBER: [{"rule": "datatype", "datatype": list},
                                           {"rule": "collection_format", "datatype": list,
                                            "validation_rules": [{"rule": "required"}, {"rule": "phone_number"}]}],
            # constants.LEAD__LANDLINE_NUMBER: [{"rule": "datatype", "datatype": list},
            #                                   {"rule": "collection_format", "datatype": list,
            #                                   "validation_rules": [{"rule": "required"}, {"rule": "phone_number"}]}],
            constants.LEAD__EMAIL_ADDRESS: [{"rule": "email"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD__ADDRESS: [{"rule": "datatype", "datatype": str}],
            # constants.LEAD__ADDRESS: [{"rule": "datatype", "datatype": dict},
            #                           {"rule": "collection_format", "datatype": dict,
            #                            "validation_rules": {
            #                                "key": [{"rule": "required"},
            #                                        {"rule": "choices", "options": constants.LEAD__ADDRESS__KEY_LIST}],
            #                                "value": [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            #                            }}],
            constants.LEAD__PROJECT: [{"rule": "datatype", "datatype": str}],
            constants.LEAD__SOURCE: [{"rule": "datatype", "datatype": str}],
            constants.LEAD__STATUS: [{"rule": "choices", "options": constants.LEAD__STATUS__LIST}],
            constants.LEAD__GENDER: [{"rule": "choices", "options": constants.GENDER_LIST}],
            constants.LEAD__COUNTRY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD__CITY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.LEAD__COMMENT: [{"rule": "datatype", "datatype": str}],
            constants.LEAD__CLIENT_CATEGORY: [{"rule": "choices", "options": constants.LEAD__CLIENT_CATEGORY__LIST}],
            constants.LEAD__LEVEL: [{"rule": "choices", "options": constants.LEAD__LEVEL__LIST}],

        }

    @classmethod
    def update_validation_rules(cls): return {
        constants.LEAD__FIRST_NAME: [{"rule": "nonexistent"}],
        constants.LEAD__STATUS: [{"rule": "nonexistent"}],
        constants.LEAD__GENDER: [{"rule": "nonexistent"}],
        constants.LEAD__COUNTRY: [{"rule": "nonexistent"}],
        constants.LEAD__CITY: [{"rule": "nonexistent"}],
    }

    first_name = db.StringField(required=True)
    last_name = db.StringField()
    nic = db.StringField()
    # phone_number = db.ListField(db.StringField())
    # landline_number = db.ListField(db.StringField())
    phone_number = db.ListField()
    landline_number = db.StringField()
    email_address = db.StringField()
    address = db.StringField()
    # address = db.DictField(db.StringField())
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
    lead_id = db.SequenceField(value_decorator='LD-{}'.format)
    transfered = db.BooleanField(default=False)
    followup_id = db.StringField()
    followup_type = db.StringField()
    followup_last_work = db.StringField()
    followup_next_task = db.StringField()
    followup_ref_id = db.StringField()
    followup_last_work_date = db.IntField()
    followup_count = db.IntField()
    next_deadline = db.DateTimeField()
    transfered_on = db.IntField()

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.LEAD__ID: self[constants.LEAD__ID],
            constants.LEAD__FIRST_NAME: self[constants.LEAD__FIRST_NAME],
            constants.LEAD__LAST_NAME: self[constants.LEAD__LAST_NAME],
            constants.LEAD__NIC: self[constants.LEAD__NIC],
            constants.LEAD__PHONE_NUMBER: self[constants.LEAD__PHONE_NUMBER],
            constants.LEAD__LANDLINE_NUMBER: self[constants.LEAD__LANDLINE_NUMBER],
            constants.LEAD__EMAIL_ADDRESS: self[constants.LEAD__EMAIL_ADDRESS],
            constants.LEAD__ADDRESS: self[constants.LEAD__ADDRESS],
            constants.LEAD__PROJECT: self[constants.LEAD__PROJECT],
            constants.LEAD__SOURCE: self[constants.LEAD__SOURCE],
            constants.LEAD__STATUS: self[constants.LEAD__STATUS],
            constants.LEAD__GENDER: self[constants.LEAD__GENDER],
            constants.LEAD__COUNTRY: self[constants.LEAD__COUNTRY],
            constants.LEAD__CITY: self[constants.LEAD__CITY],
            constants.LEAD__CLIENT_CATEGORY: self[constants.LEAD__CLIENT_CATEGORY],
            constants.LEAD__LEVEL: self[constants.LEAD__LEVEL],
            constants.LEAD__COMMENT: self[constants.LEAD__COMMENT],
            constants.LEAD__ASSIGNED_TO: self[constants.LEAD__ASSIGNED_TO].fetch().name,
            constants.LEAD__ASSIGNED_BY: self[constants.LEAD__ASSIGNED_BY].fetch().name,
            constants.LEAD__TRANSFERED: self[constants.LEAD__TRANSFERED] if self[constants.LEAD__TRANSFERED] else False,
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self.created_by.fetch().name,
            constants.CREATED_ON: self[constants.CREATED_ON],
            constants.UPDATED_ON: self[constants.UPDATED_ON],
            constants.LEAD__TRANSFERED_ON: self[constants.LEAD__TRANSFERED_ON] if self[constants.LEAD__TRANSFERED_ON] else False
        }

    def display_transfer(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.LEAD__ID: self[constants.LEAD__ID],
            constants.LEAD__FIRST_NAME: self[constants.LEAD__FIRST_NAME],
            constants.LEAD__LAST_NAME: self[constants.LEAD__LAST_NAME],
            constants.LEAD__NIC: self[constants.LEAD__NIC],
            constants.LEAD__PHONE_NUMBER: self[constants.LEAD__PHONE_NUMBER],
            constants.LEAD__LANDLINE_NUMBER: self[constants.LEAD__LANDLINE_NUMBER],
            constants.LEAD__EMAIL_ADDRESS: self[constants.LEAD__EMAIL_ADDRESS],
            constants.LEAD__ADDRESS: self[constants.LEAD__ADDRESS],
            constants.LEAD__PROJECT: self[constants.LEAD__PROJECT],
            constants.LEAD__SOURCE: self[constants.LEAD__SOURCE],
            constants.LEAD__STATUS: self[constants.LEAD__STATUS],
            constants.LEAD__GENDER: self[constants.LEAD__GENDER],
            constants.LEAD__COUNTRY: self[constants.LEAD__COUNTRY],
            constants.LEAD__CITY: self[constants.LEAD__CITY],
            constants.LEAD__CLIENT_CATEGORY: self[constants.LEAD__CLIENT_CATEGORY],
            constants.LEAD__LEVEL: self[constants.LEAD__LEVEL],
            constants.LEAD__COMMENT: self[constants.LEAD__COMMENT],
            constants.LEAD__ASSIGNED_TO: self[constants.LEAD__ASSIGNED_TO],
            constants.LEAD__ASSIGNED_BY: self[constants.LEAD__ASSIGNED_BY],
            constants.LEAD__TRANSFERED: self[constants.LEAD__TRANSFERED] if self[constants.LEAD__TRANSFERED] else False,
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self.created_by.fetch().name,
            constants.CREATED_ON: self[constants.CREATED_ON],
            constants.UPDATED_ON: self[constants.UPDATED_ON]
        }

    def display_min(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.LEAD__ID: self[constants.LEAD__ID],
            constants.LEAD__FIRST_NAME: self[constants.LEAD__FIRST_NAME],
            constants.LEAD__PHONE_NUMBER: self[constants.LEAD__PHONE_NUMBER],
            constants.LEAD__PROJECT: self[constants.LEAD__PROJECT],
            constants.LEAD__LEVEL: self[constants.LEAD__LEVEL],
            constants.LEAD__ASSIGNED_TO: self[constants.LEAD__ASSIGNED_TO].fetch().name,
            constants.CREATED_ON: common_utils.epoch_to_datetime(self[constants.CREATED_ON]),
            constants.LEAD__LAST_WORK_DATE: common_utils.epoch_to_datetime(self[constants.LEAD__LAST_WORK_DATE]),
            constants.LEAD__LAST_WORK: self[constants.LEAD__LAST_WORK],
            constants.LEAD__FOLLOWUP_COUNT: self[constants.LEAD__FOLLOWUP_COUNT],
            'new': 'NEW' if self[constants.UPDATED_ON] == constants.LEAD__TRANSFERED else ''
        }