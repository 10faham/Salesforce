# Python imports

# Local imports
from ppBackend.generic import models, db
from ppBackend.generic.services.utils import constants
from ppBackend.UserManagement.models.User import User


class Token(models.Model):
    @classmethod
    def validation_rules(self):
        return {
            constants.TOKEN__ACCESS_TOKEN: [
                {"rule": "required"},
                {"rule": "unique",
                 "Model": self,
                 "Field": constants.TOKEN__ACCESS_TOKEN}],
            constants.TOKEN__USER: [
                {"rule": "required"},
                {"rule": "exists",
                 "Model": User,
                 "Field": constants.ID}],
            constants.TOKEN__PURPOSE: [
                {"rule": "required"},
                {"rule": "choices",
                 "options": [constants.PURPOSE_LOGIN,
                             constants.PURPOSE_RESET_PASSWORD]}],
            constants.TOKEN__EXPIRY_TIME: [{"rule": "required"}],
            constants.TOKEN__IS_EXPIRED: [],
            constants.TOKEN__IS_REVOKED: [],
        }

    @ classmethod
    def update_validation_rules(self): return{
    }
    access_token = db.StringField(required=True, unique=True)
    user = db.ReferenceField(User, required=True)
    purpose = db.StringField(required=True)
    expiry_time = db.IntField(required=True)
    is_expired = db.BooleanField(default=False)
    is_revoked = db.BooleanField(default=False)

    def display(self):
        return {
            constants.TOKEN__ACCESS_TOKEN: self.access_token,
            constants.TOKEN__USER: self.user.display(),
            constants.TOKEN__PURPOSE: self.purpose,
            constants.TOKEN__EXPIRY_TIME: self.expiry_time,
            constants.TOKEN__IS_EXPIRED: self.is_expired,
            constants.TOKEN__IS_REVOKED: self.is_revoked,
            constants.STATUS: self.status
        }
