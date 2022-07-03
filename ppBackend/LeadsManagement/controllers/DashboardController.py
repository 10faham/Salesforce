# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from ppBackend import config
from datetime import datetime, date, time


class DashboardController(Controller):
    Model = Leads

    @classmethod
    def read_lead_count(cls, data, filter={}):
        lead_data = []
        user = common_utils.current_user()
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.UPDATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.UPDATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
        else:
            datefrom = datetime.combine(datetime.now().date(), time(0,0)).strftime(config.DATETIME_FORMAT)
            dateto = datetime.combine(datetime.now().date(), time(23,59,59)).strftime(config.DATETIME_FORMAT)
            filter[constants.UPDATED_ON+"__gte"] = common_utils.convert_to_epoch1000(datefrom)
            filter[constants.UPDATED_ON+"__lte"] = common_utils.convert_to_epoch1000(dateto)

        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(
                data.get(constants.LEAD__ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]

        filter[constants.LEAD__ASSIGNED_TO +
               "__in"] = [str(id) for id in user_ids]

        queryset = cls.db_read_records(
            read_filter={**filter}).aggregate(pipeline.KPI_REPORT_LEAD_COUNT)
        for user in queryset:
            tmp = UserController.get_user(user['_id'])
            lead_data.append(
                {'id': str(tmp.pk), 'username': tmp[constants.USER__NAME], 'lead_count': user['lead_count'], 'transfered': user['transfered']})
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=lead_data
        )


class DashboardFollow(Controller):
    Model = FollowUp

    @classmethod
    def read_follow(cls, data):
        user = common_utils.current_user()
        follow_dataset = []
        queryset = cls.db_read_records(
            read_filter={constants.CREATED_BY: user})

        follow_dataset.append([queryset.count()])
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=follow_dataset
        )

    @classmethod
    def read_kpi(cls, data, data2=None):
        # user = common_utils.current_user()
        filter = {}
        # print(data)
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
        else:
            datefrom = datetime.combine(datetime.now().date(), time(0,0)).strftime(config.DATETIME_FORMAT)
            dateto = datetime.combine(datetime.now().date(), time(23,59,59)).strftime(config.DATETIME_FORMAT)
            filter[constants.CREATED_ON+"__gte"] = common_utils.convert_to_epoch1000(datefrom)
            filter[constants.CREATED_ON+"__lte"] = common_utils.convert_to_epoch1000(dateto)
            datefrom = datetime.combine(datetime.now().date(), time(0,0)).strftime("%d %m %Y %H:%M:%S")
            dateto = datetime.combine(datetime.now().date(), time(23,59,59)).strftime("%d %m %Y %H:%M:%S")

        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(
                data.get(constants.LEAD__ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]
        # user_ids = [id(constants.ID) for id in user_childs]

        filter[constants.CREATED_BY+"__in"] = [str(id) for id in user_ids]
        # queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **filter, **data})

        # queryset = cls.db_read_records(read_filter={**filter})
        queryset = cls.db_read_records(read_filter={**filter}).aggregate(
            pipeline.KPI_REPORT_FOLLOW_UP)
        kpi_dataset = {str(user[constants.ID]): {
            "name": user[constants.USER__NAME],
            "Call": {"_sum": 0, "_connected": 0},
            "Meeting": {"_sum": 0, "_connected": 0},
            "Sale": {"_sum": 0, "_connected": 0},
            "Email": {"_sum": 0, "_connected": 0},
            "Acquisition": {"_sum": 0, "_connected": 0},
            "TLW": 0,
            "lead_count": 0,
            "transfered":0
        } for user in user_childs}
        for user in queryset:
            # if user["_id"]["created_by"] not in user_ids:
            #     continue
            kpi_dataset[str(user["_id"]["created_by"])][user["_id"]
                                                        ['type']][user["_id"]['sub_type']] = user["count"]
            kpi_dataset[str(user["_id"]["created_by"])][user["_id"]
                                                        ['type']]["_sum"] += user['count']
            kpi_dataset[str(user["_id"]["created_by"])]['TLW'] += user['count']
            if user["_id"]['sub_type'] == 'Contacted_client' or user["_id"]['sub_type'] == 'Followed_up':
                kpi_dataset[str(user["_id"]["created_by"])][user["_id"]
                                                            ['type']]['_connected'] += user["count"]
        if data2.get('response_code'):
            for obj in data2.get('response_data'):
                kpi_dataset[obj['id']]['lead_count'] = int(obj['lead_count'])- int(obj['transfered'])
                kpi_dataset[obj['id']]['transfered'] = obj['transfered']
        # for user in queryset:
        #     if user['_id']['created_by'] in user_ids:
        #         temp.append(user['_id'])
        # temp.append(user['_id'] for user in queryset if user['_id']['created_by'] in user_childs)
        # temp = list(queryset)

        # for user in follow_dataset:
        #     calls = 0
        #     meetings = 0
        #     at_calls = 0
        #     v_calls = 0
        #     for follow in user[1]:
        #         if follow['type'] == 'Call':
        #             calls += 1
        #         elif follow['type'] == 'Meeting':
        #             meetings += 1
        #         if follow['sub_type'] == 'Contacted_client' or "Followed_up" or "Whatsapp_call" or "Meeting_Confirmed" or 'Meeting_cancelled' or "Meeting_postponed":
        #             v_calls += 1
        #         elif follow['sub_type'] == 'Call_attempt':
        #             at_calls += 1
        #     kpi_dataset.append(
        #         [user[0], calls, meetings, len(user[1]), at_calls, v_calls])
        out_data = {
            'kpi': kpi_dataset,
            'dateto': dateto,
            'datefrom': datefrom
        }
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=out_data
        )
# '619dd065945a75460afc2214'
