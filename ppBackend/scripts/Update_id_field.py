# Date Created 22/05/2022 00:00:00


# Local imports
from ppBackend import app
from ppBackend.config import config
from ppBackend.generic.services.utils import common_utils, constants
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController

# from ppBackend.UserManagement.controllers.RoleController\
#     import RoleController


def update_id_field(run=False):
    if not run:
        return
    with app.test_request_context():
        count = 0
        queryset = LeadsController.db_read_records(read_filter={}, deleted_records=True)
        for index, obj in enumerate(queryset):
            obj['lead_id'] = f'LD-{index + 1}'
            obj.save()
            count += 1
            print("Updated Obj :", obj)
            print(count)
        queryset = FollowUpController.db_read_records(read_filter={}, deleted_records=True)
        count = 0
        for index, obj in enumerate(queryset):
            obj['follow_id'] = f'FL-{index + 1}'
            obj.save()
            count += 1
            print("Updated Obj :", obj)
            print(count)
