# Python imports

# Framework imports

# Local imports
from ppBackend.generic import models
from ppBackend.generic import db
from ppBackend.generic.services.utils import constants
from ppBackend.LeadsManagement.models.Lead import Leads


class FollowUp(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.FOLLOW_UP__LEAD: [
                {"rule": "required"},
                {"rule": "fetch_obj", "Field": constants.ID, "ObjField": constants.FOLLOW_UP__LEAD}],
            constants.FOLLOW_UP__NEXT: [{"rule": "datetime_format"}],
            constants.FOLLOW_UP__COMMENT: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str}],
            constants.FOLLOW_UP__STATUS: [
                {"rule": "required"},
                {"rule": "choices", "options": constants.FOLLOW_UP__STATUS__LIST}],
            constants.FOLLOW_UP__LEVEL: [
                {"rule": "required"},
                {"rule": "choices", "options": constants.FOLLOW_UP__LEVEL__LIST}],
        }

    @ classmethod
    def update_validation_rules(cls): return {
        constants.LEAD__FIRST_NAME: [{"rule": "nonexistent"}],
    }

    lead = db.LazyReferenceField(Leads, required=True)
    next = db.DateTimeField()
    comment = db.StringField(required=True)
    lead_status = db.StringField(required=True)
    lead_level = db.StringField(required=True)

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.FOLLOW_UP__LEAD: self[constants.FOLLOW_UP__LEAD].fetch().display(),
            constants.FOLLOW_UP__NEXT: self[constants.FOLLOW_UP__NEXT].fetch().display(),
            constants.FOLLOW_UP__COMMENT: self[constants.FOLLOW_UP__COMMENT],
            constants.FOLLOW_UP__STATUS: self[constants.FOLLOW_UP__STATUS],
            constants.FOLLOW_UP__LEVEL: self[constants.FOLLOW_UP__LEVEL],
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self[constants.CREATED_BY].fetch()[
                constants.USER__NAME]
        }
