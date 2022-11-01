# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from ppBackend import config
from datetime import datetime, date, time, timedelta


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
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
        else:
            datefrom = datetime.combine(datetime.now().date(), time(
                0, 0)).strftime(config.DATETIME_FORMAT)
            dateto = datetime.combine(datetime.now().date(), time(
                23, 59, 59)).strftime(config.DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto)

        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(
                data.get(constants.LEAD__ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]

        filter[constants.CREATED_BY +
               "__in"] = [str(id) for id in user_ids]

        queryset = cls.db_read_records(
            read_filter={**filter}).aggregate(pipeline.KPI_REPORT_LEAD_COUNT)        
        for user in queryset:
            tmp = UserController.get_user(user['_id'])
            lead_data.append(
                {'id': str(tmp.pk), 'username': tmp[constants.USER__NAME], 'lead_count': user['lead_count']})

        lead_transfer = []
        filter[constants.LEAD__TRANSFERED_ON + "__gte"] = filter[constants.CREATED_ON + "__gte"]
        filter[constants.LEAD__TRANSFERED_ON + "__lte"] = filter[constants.CREATED_ON + "__lte"]
        filter[constants.LEAD__ASSIGNED_TO + "__in"] = filter[constants.CREATED_BY + "__in"]
        del filter[constants.CREATED_BY + "__in"]
        del filter[constants.CREATED_ON + "__gte"]
        del filter[constants.CREATED_ON + "__lte"]
        queryset = cls.db_read_records(read_filter={**filter}).aggregate(pipeline.KPI_REPORT_LEADTRANSFER_COUNT)
        for user in queryset:
            tmp = UserController.get_user(user['_id'])
            lead_transfer.append(
                {'id': str(tmp.pk), 'username': tmp[constants.USER__NAME], 'transfered': user['transfered']})

        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=[lead_data, lead_transfer]
        )
    
    @classmethod
    def get_dashboard_stats(cls):
        user = common_utils.current_user()
        data = {
            "user":user[constants.USER__NAME],
            "total_leads" : 0,
            "new_leads" : 0,
        }
        filter = {}
        filter[constants.LEAD__ASSIGNED_TO] = user[constants.ID]

        queryset = list(cls.db_read_records(
            read_filter={**filter}).aggregate(pipeline.DASHBOARD_LEAD_COUNT))
        if queryset:
            if len(queryset) > 1:
                data['total_leads'] = queryset[0]["total"] + queryset[1]["total"]
                data['new_leads'] = queryset[0]["new"]
            else:
                data['total_leads'] = queryset[0]["total"]
                data['new_leads'] = queryset[0]["new"]

        followup_dataset = []
        overdue = 0
        today = 0

        queryset = FollowUpController.db_read_records(read_filter={**filter}).aggregate(pipeline.LAST_FOLLOWUP)
        followup_dataset = [obj for obj in queryset]
        for item in followup_dataset:
            now = datetime.utcnow().date()
            if item['deadline'].date() < now:
                overdue += 1
            if item['deadline'].date() == now:
                today += 1
        data["overdue"] = overdue
        data["today"] = today

        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=data
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
            datefrom = datetime.combine(datetime.now().date(), time(
                0, 0)).strftime(config.DATETIME_FORMAT)
            dateto = datetime.combine(datetime.now().date(), time(
                23, 59, 59)).strftime(config.DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto)
            datefrom = datetime.combine(datetime.now().date(), time(
                0, 0)).strftime("%d %m %Y %H:%M:%S")
            dateto = datetime.combine(datetime.now().date(), time(
                23, 59, 59)).strftime("%d %m %Y %H:%M:%S")

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
            pipeline.KPI_REPORT_LEAD)
        kpi_dataset = {str(user[constants.ID]): {
            "name": user[constants.USER__NAME],
            "Call": {"_sum": 0, "_connected": 0},
            "Meeting": {"_sum": 0, "_connected": 0},
            "Sale": {"_sum": 0, "_connected": 0},
            "Email": {"_sum": 0, "_connected": 0},
            "Acquisition": {"_sum": 0, "_connected": 0},
            "TLW": 0,
            "lead_count": 0,
            "transfered": 0
        } for user in user_childs}
        for user in queryset:
            # if user["_id"]["created_by"] not in user_ids:
            #     continue
            kpi_dataset[str(user["_id"]["assigned_to"])][user["_id"]
                                                        ['type']][user["_id"]['sub_type']] = user["count"]
            kpi_dataset[str(user["_id"]["assigned_to"])][user["_id"]
                                                        ['type']]["_sum"] += user['count']
            kpi_dataset[str(user["_id"]["assigned_to"])]['TLW'] += user['count']
            if user["_id"]['sub_type'] == 'Contacted_client' or user["_id"]['sub_type'] == 'Followed_up':
                kpi_dataset[str(user["_id"]["assigned_to"])][user["_id"]
                                                            ['type']]['_connected'] += user["count"]
        if data2.get('response_code'):
            for obj in data2.get('response_data')[0]:
                kpi_dataset[obj['id']]['lead_count'] = obj['lead_count']
            for obj in data2.get('response_data')[1]:
                kpi_dataset[obj['id']]['transfered'] = obj['transfered']

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
