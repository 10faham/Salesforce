# Date Created 14/09/2021 17:05:00


# Local imports
from asyncore import read
from ppBackend import app, config
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.generic.services.utils import constants, pipeline
from datetime import datetime

# from ppBackend.UserManagement.controllers.RoleController\
#     import RoleController


def find_missing(run=False):
    if not run:
        return
    with app.test_request_context():
        count = 0
        missing = 0
        miss = []
        queryset = FollowUpController.db_read_records(read_filter={}).order_by("_id")
        for item in queryset:
            try:
                lead = LeadsController.db_read_single_record(read_filter={constants.ID:str(item[constants.FOLLOW_UP__LEAD].fetch().id)})
                if lead:
                    count += 1
                    print("count {}-{}".format(count, item[constants.FOLLOWUP__ID]))
                else:
                    missing += 1
                    print('missing {}'.format(missing))
                    miss.append(item[constants.FOLLOWUP__ID])
            except Exception as e:
                missing += 1
                miss.append(item[constants.FOLLOWUP__ID])
        print('missing {}'.format(missing))
        print("count {}".format(count))
        print(miss)