# Python imports

# Framework imports

# Local imports
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.models.FollowUp import FollowUp
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from ppBackend import config
from datetime import datetime, date, time, timedelta
from functools import reduce 


class ReportsController(Controller):
    Model = Leads

    @classmethod
    def read_lead_new(cls, data, filter={}):
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM)
            dateto = data.get(constants.DATE_TO)
            if data.get(constants.LEAD__TRANSFERED) == 'true':
                filter[constants.LEAD__TRANSFERED_ON +
                    "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
                filter[constants.LEAD__TRANSFERED_ON +
                    "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
                filter[constants.LEAD__ASSIGNED_TO] = data.get(constants.ID)
                filter[constants.LEAD__TRANSFERED] = True
            else:
                filter[constants.CREATED_ON +
                    "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
                filter[constants.CREATED_ON +
                    "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
                filter[constants.CREATED_BY] = data.get(constants.ID)
                # filter[constants.LEAD__TRANSFERED] = False

        queryset = cls.db_read_records(read_filter=filter)
        queryset = queryset.aggregate(pipeline.ALL_LEADS)
        lead_data = [obj for obj in queryset]
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=lead_data
        )

    @classmethod
    def read_followup(cls, data):
        filter = {}
        filter_data = {**data}
        filter_fields = {
            "project":constants.PROJECT,
            "level": constants.LEAD__LEVEL__LIST,
            "Task": constants.FOLLOW_UP__TYPE_LIST,
            "Team": [],
        }
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
                
        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.LEAD__ASSIGNED_TO))]
            filter_data['assigned_to_name'] = user_childs[0]['name']
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]
        filter[constants.CREATED_BY+"__in"] = [str(id) for id in user_ids]

        if data.get('Task'):
            filter[constants.FOLLOW_UP__TYPE] = data.get('Task')
        
        if data.get('sub_task'):
            filter[constants.FOLLOW_UP__SUB_TYPE + "__in"] = data.get('sub_task').split(',')

        if data.get('page'):
            page = int(data['page'])
        else:
            page = 1
        
        if data.get('per_page'):
            per_page = int(data('per_page'))
        else:
            per_page = 50

        if data.get('lead_id'):
            filter[constants.LEAD__ID] = data.get('lead_id')
        queryset = FollowUpController.db_read_records(read_filter={**filter}).aggregate(
            pipeline.KPI_REPORT_FOLLOW_UP)
        followups_list = []
        for obj in queryset:
            followups_list.append(obj['ids'])
        followups = reduce(lambda a, b: a+b, followups_list)
        queryset = FollowUpController.db_read_records(read_filter={constants.ID+"__in":followups}).order_by('-id').paginate(page=page, per_page=per_page)
        followup_dataset = [obj.display_min() for obj in queryset.items]
        temp = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        all_users = []
        for id in temp:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        followup_data = {}
        followup_data['data'] = followup_dataset
        followup_data['username'] = common_utils.current_user()[
            constants.USER__NAME]
        followup_data['userlevel'] = common_utils.current_user()[
            constants.USER__ROLE][constants.USER__ROLE__ROLE_ID]
        followup_data['all_users'] = all_users
        followup_data['pagination'] = {
            "next_num" : queryset.next_num,
            "page" : queryset.page,
            "pages" : queryset.pages,
            "per_page" : queryset.per_page,
            "prev_num" : queryset.prev_num,
            "total" : queryset.total,
            "has_next" : queryset.has_next,
            "has_prev" : queryset.has_prev
        }
        followup_data['filter_fields'] = filter_fields
        followup_data['filter_data'] = filter_data
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=followup_data
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
            datefrom = datefrom[:11]
            dateto = dateto[:11]
        else:
            datefrom = datetime.combine(datetime.now().date(), time(
                0, 0)).strftime(config.DATETIME_FORMAT)
            dateto = datetime.combine(datetime.now().date(), time(
                23, 59, 59)).strftime(config.DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto)
            datefrom = datetime.now().date().strftime("%d %m %Y")
            dateto = datetime.now().date().strftime("%d %m %Y")

        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(
                data.get(constants.CREATED_BY))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]
        # user_ids = [id(constants.ID) for id in user_childs]

        filter[constants.CREATED_BY+"__in"] = [str(id) for id in user_ids]
        # queryset = cls.db_read_records(read_filter={constants.CREATED_BY: user, **filter, **data})

        # queryset = cls.db_read_records(read_filter={**filter})
        queryset = FollowUpController.db_read_records(read_filter={**filter}).aggregate(
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
            "transfered": 0
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
        queryset = FollowUpController.db_read_records(read_filter={**filter}).aggregate(
            pipeline.KPI_REPORT_FOLLOW_UP_MEETINGS)
        for user in queryset:
            kpi_dataset[str(user["_id"]["created_by"])][user["_id"]
                                            ['next_task']] = user["count"]
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