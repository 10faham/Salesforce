# Date Created 22/05/2022 00:00:00


# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
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
        # for index, obj in enumerate(queryset):
        #     obj['lead_id'] = f'LD-{index + 1}'
        #     obj.save()
        #     count += 1
        #     print("Updated Obj :", obj)
        #     print(count)
        new = {}
        for lead in queryset:
            new[constants.LEAD__PHONE_NUMBER] = [lead[constants.LEAD__PHONE_NUMBER]]
            new[constants.ID] = str(lead[constants.ID])

            res = LeadsController.db_update_single_record(read_filter = {constants.ID:lead[constants.ID]}, update_filter = new, deleted_records=True)
            count += 1
            print(count)
            print(res)
        # queryset = FollowUpController.db_read_records(read_filter={}, deleted_records=True)
        # count = 0
        # for index, obj in enumerate(queryset):
        #     obj['follow_id'] = f'FL-{index + 1}'
        #     obj.save()
        #     count += 1
        #     print("Updated Obj :", obj)
        #     print(count)

        # queryset = LeadsHistoryController.db_read_records(read_filter={}, deleted_records=True)
        # count = 0
        # for index, obj in enumerate(queryset):
        #     obj['history_id'] = f'LH-{index + 1}'
        #     obj.save()
        #     count += 1
        #     print("Updated Obj :", obj)
        #     print(count)
