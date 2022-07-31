# Date Created 14/09/2021 17:05:00


# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
from ppBackend.generic.services.utils import constants, pipeline



def junk_follow_up_lead_history_removal(run=False):
    if not run:
        return
    with app.test_request_context():
        # followUps = FollowUpController.db_read_records(read_filter={
        #     constants.FOLLOW_UP__ASSIGNED_TO: '62b3078dd33ee5b92aa2e6ae',
        #     constants.FOLLOW_UP__COMMENT: "7412"})
        # followUps = followUps.aggregate([
        #     {
        #         '$group': {
        #             '_id': '$lead',
        #             'all_id': {
        #                 '$addToSet': '$_id'
        #             }
        #         }
        #     }
        # ])
        # followupss = list(followUps)
        # del_followUp = []
        # for follow in followupss:
        #     del_followUp.extend(follow["all_id"])
        # print("del_followUp", del_followUp)
        # followaUps = "[ObjectId('" + "'),ObjectId('".join(map(str, del_followUp)) + "')]"
        # print("del_followUp", followaUps)

        # leadGroups = LeadsHistoryController.db_read_records(read_filter={}).aggregate([
        #     {
        #         '$group': {
        #             '_id': '$lead_id',
        #             'all_id': {
        #                 '$addToSet': '$_id'
        #             }
        #         }
        #     }
        # ])
        # leads = list(leadGroups)
        # del_history = []
        # for leadGroup in leads:
        #     del_history.extend(leadGroup["all_id"][1:])
        # string = "[ObjectId('" + \
        #     "'),ObjectId('".join(map(str, del_history)) + "')]"
        # print("string", string)
        data = {}
        count = 0
        tania = 0
        taha = 0
        taha2 = 0
        taha3 = 0
        lead1 = 0
        lead2 = 0
        lead3 = 0
        lead4 = 0
        data['transfer_to'] = '619dd065945a75460afc2214'
        # queryset = FollowUpController.db_read_records(read_filter={'assigned_to':data['transfer_to']}).aggregate(pipeline.LAST_FOLLOWUP)
        # followup_dataset = [obj for obj in queryset]
        # print(followup_dataset)
        # for follow in followup_dataset:
        #     count += 1
        #     followups = FollowUpController.read_lead_follow(data = {'lead':follow['_id'], 'name':'', 'ref':''})
        #     total = len(followups['response_data'][0])
        #     if total >= 2:
        #         last_f = str(followups['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
        #         last_ff = str(followups['response_data'][0][total-2][constants.CREATED_BY].fetch()[constants.ID])
        #         # last_fff = str(followups['response_data'][0][total-3][constants.CREATED_BY].fetch()[constants.ID])
        #         if last_f == '619b5e56360643a46baf381c' and last_ff == '619b5e56360643a46baf381c':
        #             lead = LeadsController.db_read_single_record(read_filter={constants.ID:followups['response_data'][0][total-1]['lead']['id'], 'assigned_to':data['transfer_to']})
        #             if lead:
        #                 lead1 += 1
        #             tania += 1
        #     if total >= 2:
        #         last_f = str(followups['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
        #         last_ff = str(followups['response_data'][0][total-2][constants.CREATED_BY].fetch()[constants.ID])
        #         if last_f == '619b5e56360643a46baf381c' and last_ff == data['transfer_to']:
        #             lead = LeadsController.db_read_single_record(read_filter={constants.ID:followups['response_data'][0][total-1]['lead']['id'], 'assigned_to':data['transfer_to']})
        #             if lead:
        #                 lead2 += 1
        #             taha += 1
        #     if total >= 2:
        #         last_f = str(followups['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
        #         last_ff = str(followups['response_data'][0][total-2][constants.CREATED_BY].fetch()[constants.ID])
        #         if last_f != data['transfer_to'] and last_ff != data['transfer_to']:
        #             lead = LeadsController.db_read_single_record(read_filter={constants.ID:followups['response_data'][0][total-1]['lead']['id'], 'assigned_to':data['transfer_to']})
        #             if lead:
        #                 lead3 += 1
        #             taha2 += 1
        #     if total >= 1:
        #         last_f = str(followups['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
        #         if last_f == data['transfer_to']:
        #             lead = LeadsController.db_read_single_record(read_filter={constants.ID:followups['response_data'][0][total-1]['lead']['id'], 'assigned_to':data['transfer_to']})
        #             if lead:
        #                 lead4 += 1
        #             taha3 += 1
        #     print("count {}".format(count))
        # print("tania {} - {}".format(tania, lead1))
        # print("taha {} - {}".format(taha, lead2))
        # print("taha2 {} - {}".format(taha2, lead3))
        # print("taha3 {} - {}".format(taha3, lead4))

        leadh = LeadsHistoryController.db_read_records(read_filter={"created_by":'619b5e56360643a46baf381c', "created_on__gte":1658793600000, "created_on__lte":1658879999000, "assigned_to":data['transfer_to']})
        for lead in leadh:
            followup = FollowUpController.read_lead_follow(data = {'lead':lead['lead_id'], 'name':'', 'ref':''})
            total = len(followup['response_data'][0])
            # transfer_to = str(followup['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
            count +=1
            print(count)
            for follow in followup['response_data'][0]:
                followup_updatedata = {constants.FOLLOW_UP__ASSIGNED_TO: data['transfer_to'],
                constants.ID: follow[constants.ID]}
                res = FollowUpController.update_controller(followup_updatedata)

            leads = {}
            # leads[constants.LEAD__FOLLOWUP] = res['response_data'][constants.ID]
            leads[constants.ID] = lead['lead_id']
            # leads[constants.LEAD__COMMENT] = res['response_data'][constants.FOLLOW_UP__COMMENT]
            leads[constants.LEAD__LEVEL] = lead['lead_level']
            # leads[constants.LEAD__LAST_WORK] = res['response_data']['sub_type']
            # leads[constants.LEAD__LAST_WORK_DATE] = res['response_data']['created_on']
            # leads[constants.LEAD__FOLLOWUP_TYPE] = res['response_data']['type']
            # leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = res['response_data']['next_deadline']
            # leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = res['response_data']['next_task']
            # leads[constants.LEAD__PROJECT] = res['response_data']['next_project']
            leads[constants.LEAD__ASSIGNED_TO] = data['transfer_to']
            # leads[constants.LEAD__ASSIGNED_BY] = common_utils.current_user()
            leads[constants.LEAD__TRANSFERED] = False
            # leads[constants.LEAD__TRANSFERED_ON] = common_utils.get_time()
            res = LeadsController.db_update_single_record(read_filter = {constants.ID:res['response_data'][constants.FOLLOW_UP__LEAD]['id']}, update_filter = leads)
            print(res)