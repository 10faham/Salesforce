# Python imports

# Framework imports

# Local imports
from ppBackend.generic import models
from ppBackend.generic import db
from ppBackend.generic.services.utils import constants
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.UserManagement.models.User import User


class FollowUp(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.FOLLOW_UP__LEAD: [
                {"rule": "required"},
                {"rule": "fetch_obj", "Model": Leads, "Field": constants.ID, "ObjField": constants.FOLLOW_UP__LEAD}],
            constants.FOLLOW_UP__TYPE: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str}],
            constants.FOLLOW_UP__SUB_TYPE: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str}],
            constants.FOLLOW_UP__LEVEL: [
                {"rule": "required"},
                {"rule": "choices", "options": constants.FOLLOW_UP__LEVEL__LIST}],
            constants.FOLLOW_UP__STATUS: [
                {"rule": "choices", "options": constants.FOLLOW_UP__STATUS__LIST}],
            constants.FOLLOW_UP__COMPLETION_DATE: [
                {"rule": "required"}, 
                {"rule": "datetime_format"}],
            constants.FOLLOW_UP__COMMENT: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str}],
            constants.FOLLOW_UP__NEXT_TASK: [
                {"rule": "required"},
                {"rule": "datatype", "datatype": str}],
            constants.FOLLOW_UP__NEXT_PROJECT: [
                {"rule": "datatype", "datatype": str}],
            constants.FOLLOW_UP__NEXT_DEADLINE: [{"rule": "required"}, {"rule": "datetime_format"}],
            constants.FOLLOW_UP__NEXT_COMMENT: [
                {"rule": "datatype", "datatype": str}],
        }

    @ classmethod
    def update_validation_rules(cls): return {
        constants.FOLLOW_UP__TYPE: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__SUB_TYPE: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__LEVEL: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__STATUS: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__COMPLETION_DATE: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__COMMENT: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__NEXT_TASK: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__NEXT_DEADLINE: [{"rule": "nonexistent"}],
        constants.FOLLOW_UP__LEAD: [{"rule": "nonexistent"}]
    }

    lead = db.LazyReferenceField(Leads, required=True)
    type = db.StringField(required=True)
    sub_type = db.StringField(required=True)
    lead_level = db.StringField(required=True)
    lead_status = db.StringField()
    completion_date = db.DateTimeField(required=True)
    comment = db.StringField(required=True)
    next_task = db.StringField(required=True)
    next_project = db.StringField()
    next_deadline = db.DateTimeField(required=True)
    next_comment = db.StringField()
    follow_id = db.SequenceField(value_decorator='FL-{}'.format)
    assigned_to = db.LazyReferenceField(User, required=True)

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.FOLLOWUP__ID: self[constants.FOLLOWUP__ID],
            constants.FOLLOW_UP__LEAD: self[constants.FOLLOW_UP__LEAD].fetch().display(),
            constants.FOLLOW_UP__TYPE: self[constants.FOLLOW_UP__TYPE],
            constants.FOLLOW_UP__SUB_TYPE: self[constants.FOLLOW_UP__SUB_TYPE],
            constants.FOLLOW_UP__LEVEL: self[constants.FOLLOW_UP__LEVEL],
            constants.FOLLOW_UP__STATUS: self[constants.FOLLOW_UP__STATUS],
            constants.FOLLOW_UP__COMPLETION_DATE: self[constants.FOLLOW_UP__COMPLETION_DATE],
            constants.FOLLOW_UP__NEXT_TASK: self[constants.FOLLOW_UP__NEXT_TASK],
            constants.FOLLOW_UP__NEXT_PROJECT: self[constants.FOLLOW_UP__NEXT_PROJECT],
            constants.FOLLOW_UP__NEXT_DEADLINE: self[constants.FOLLOW_UP__NEXT_DEADLINE],
            constants.FOLLOW_UP__NEXT_COMMENT: self[constants.FOLLOW_UP__NEXT_COMMENT],
            constants.FOLLOW_UP__COMMENT: self[constants.FOLLOW_UP__COMMENT],
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self[constants.CREATED_BY],
            constants.CREATED_ON: self[constants.CREATED_ON],
            constants.FOLLOW_UP__ASSIGNED_TO: self[constants.FOLLOW_UP__ASSIGNED_TO].fetch().name if self[constants.FOLLOW_UP__ASSIGNED_TO] else None,
        }
