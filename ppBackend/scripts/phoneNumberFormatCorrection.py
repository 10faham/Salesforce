# Date Created 14/09/2021 17:05:00


# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.generic.services.utils import constants

# from ppBackend.UserManagement.controllers.RoleController\
#     import RoleController


def phone_number_format_correction(run=False):
    if not run:
        return
    with app.test_request_context():
        queryset = LeadsController.db_read_records(read_filter={
            constants.LEAD__PHONE_NUMBER+"__startswith": "03",
            # constants.LEAD__PHONE_NUMBER+"__contains": " "
        })
        for obj in queryset:
            obj[constants.LEAD__PHONE_NUMBER] = "+92" + obj[constants.LEAD__PHONE_NUMBER][1:]
            obj[constants.LEAD__PHONE_NUMBER] = obj[constants.LEAD__PHONE_NUMBER].replace(" ", "")
            obj.save()
            print("Updated Obj : ", obj)
