# Date Created 14/09/2021 17:05:00


# Local imports
from ppBackend import app
from ppBackend.LeadsManagement.controllers.LeadsController import LeadsController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
from ppBackend.generic.services.utils import common_utils, constants, pipeline



def Report_Generator(run=False):
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
        data['transfer_to'] = '6253cce240d74a484aff4cd9'
        output = []
        users = {
            'Adeel Qureshi':0,
            'Hafiz Taha':0,
            'Irtiza Ahsan':0,
            'Noor ul haq':0,
            'Arshad':0,
            'Taha Siddiqui':0,
            'Anwar Sheikh':0
        }
        user_list = ['Adeel Qureshi','Hafiz Taha','Irtiza Ahsan','Noor ul haq','Arshad','Taha Siddiqui','Anwar Sheikh']
        leadh = LeadsController.db_read_records(read_filter={"assigned_to":'619b5e56360643a46baf381c', 
                                        "lead_comment":"NR", "updated_on__gte":1662854400000})
        for lead in leadh:
            followup = FollowUpController.read_lead_follow(data = {'lead':lead['id'], 'name':'', 'ref':''})
            total = len(followup['response_data'][0])
            if total >= 3:
                if followup['response_data'][0][1]['created_by'] in user_list:
                    users[followup['response_data'][0][1]['created_by']] += 1
                elif followup['response_data'][0][2]['created_by'] in user_list:
                    users[followup['response_data'][0][2]['created_by']] += 1
                else:
                    user_list.append(followup['response_data'][0][2]['created_by'])
                    users[followup['response_data'][0][2]['created_by']] = 1
            # transfer_to = str(followup['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
            count +=1
            print(count)
            for follow in followup['response_data'][0]:
                tmp = []
                tmp.append(count)
                tmp.append(lead['lead_id'])
                tmp.append(follow['follow_id'])
                tmp.append(follow['created_by'])
                tmp.append(follow['lead_level'])
                tmp.append(common_utils.epoch_to_datetime(follow['created_on']))
                tmp.append(follow['comment'][:20])
                # print(tmp)
                output.append(tmp)
        with open('report.csv', 'a', encoding='UTF-8') as r:
            for row in output:
                r.write(str(row[0]))
                r.write(',')
                r.write(row[1])
                r.write(',')
                r.write(row[2])
                r.write(',')
                r.write(row[3])
                r.write(',')
                r.write(row[4])
                r.write(',')
                r.write(row[5])
                r.write(',')
                r.write(row[6].replace('\n',''))
                r.write('\n')
            for user in user_list:
                r.write(user)
                r.write(',')
                r.write(str(users[user]))
                r.write(',')
            r.write('\n')