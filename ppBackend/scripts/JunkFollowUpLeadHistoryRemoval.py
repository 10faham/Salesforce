# Date Created 14/09/2021 17:05:00


# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
from ppBackend.generic.services.utils import constants


def junk_follow_up_lead_history_removal(run=False):
    if not run:
        return
    with app.test_request_context():
        followUps = FollowUpController.db_read_records(read_filter={
            constants.FOLLOW_UP__ASSIGNED_TO: '62b3078dd33ee5b92aa2e6ae',
            constants.FOLLOW_UP__COMMENT: "7412"})
        followUps = followUps.aggregate([
            {
                '$group': {
                    '_id': '$lead',
                    'all_id': {
                        '$addToSet': '$_id'
                    }
                }
            }
        ])
        followupss = list(followUps)
        del_followUp = []
        for follow in followupss:
            del_followUp.extend(follow["all_id"])
        print("del_followUp", del_followUp)
        followaUps = "[ObjectId('" + "'),ObjectId('".join(map(str, del_followUp)) + "')]"
        print("del_followUp", followaUps)

        leadGroups = LeadsHistoryController.db_read_records(read_filter={}).aggregate([
            {
                '$group': {
                    '_id': '$lead_id',
                    'all_id': {
                        '$addToSet': '$_id'
                    }
                }
            }
        ])
        leads = list(leadGroups)
        del_history = []
        for leadGroup in leads:
            del_history.extend(leadGroup["all_id"][1:])
        string = "[ObjectId('" + \
            "'),ObjectId('".join(map(str, del_history)) + "')]"
        print("string", string)
