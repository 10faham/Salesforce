# Python imports
import pandas as pd
import re
from math import nan, isnan
# Framework imports

# Local imports
from ast import Constant
from ppBackend.generic.controllers import Controller
from ppBackend.LeadsManagement.models.Lead import Leads
from ppBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
from ppBackend.UserManagement.controllers.UserController import UserController
from ppBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from ppBackend import config
from datetime import datetime


class LeadsController(Controller):
    Model = Leads

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        current_user = common_utils.current_user()
        already_exists = cls.db_read_records(read_filter={
            constants.LEAD__PHONE_NUMBER+"__in": data[constants.LEAD__PHONE_NUMBER],
            # constants.CREATED_BY+"__nin": [current_user]
        })
        if already_exists:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_USER_ALREADY_EXIST,
                response_message=response_codes.MESSAGE_ALREADY_EXISTS_DATA,
                response_data=already_exists
            )
        data[constants.LEAD__ASSIGNED_TO] = current_user
        data[constants.LEAD__ASSIGNED_BY] = current_user
        _, _, obj = cls.db_insert_record(
            data=data, default_validation=False)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )

    @classmethod
    def read_controller(cls, data):
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
        
        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.LEAD__ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)

        user_ids = [id[constants.ID] for id in user_childs]
        filter[constants.LEAD__ASSIGNED_TO+"__in"] = [str(id) for id in user_ids]
        queryset = cls.db_read_records(read_filter={**filter}).aggregate(pipeline.ALL_LEADS)

        lead_dataset = [obj for obj in queryset]
        # lead_data = {}
        # lead_id = []
        # for obj in queryset.order_by('-'+constants.CREATED_ON):
        #     lead_id.append(str(obj[constants.ID]))
        #     lead_data[str(obj[constants.ID])] = {'data': obj.display_min()}
        #     # counter = 0
        # # final_count = 0
        # # for id in lead_id:
        # #     followup = FollowUpController.read_count(id)
        # #     if followup["count"] > 0:
        # #         final_count += 1
        # # print(final_count)
        # # for i in range(0, len(lead_id), 100):
        # followup = FollowUpController.read_current_followup(lead_id)
        # for obj in followup:
        #     lead_data[obj['_id']].update({'followup': obj})

        # for obj in queryset.order_by("-"+constants.CREATED_ON):
        #     tmp = obj.display()
        #     tmp['followup'] = FollowUpController.read_count(tmp['id'])
        #     lead_data.append(tmp)
        
        # lead_dataset.append(
            # [str(user.pk), user[constants.USER__NAME], lead_data])
        # lead_dataset.append(common_utils.current_user().name)
        temp = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        all_users = []
        for id in temp:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        leads_data = {}
        leads_data['data'] = lead_dataset
        leads_data['username'] = common_utils.current_user()[
            constants.USER__NAME]
        leads_data['userlevel'] = common_utils.current_user()[
            constants.USER__ROLE][constants.USER__ROLE__ROLE_ID]
        leads_data['all_users'] = all_users
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=leads_data
        )

    @classmethod
    def update_controller(cls, data):
        is_valid, error_messages, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]}, update_filter=data
        )
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if not obj:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.LEAD.title(), constants.ID
                ))
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display(),
        )

    @classmethod
    def suspend_controller(cls, data):
        _, _, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]},
            update_filter={
                constants.STATUS: constants.OBJECT_STATUS_SUSPENDED},
            update_mode=constants.UPDATE_MODE__PARTIAL,
        )
        if obj:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display(),
            )
        return response_utils.get_response_object(
            response_code=response_codes.CODE_RECORD_NOT_FOUND,
            response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                constants.LEAD.title(), constants.ID
            ))
    
    @classmethod
    def read_count(cls, data):
        filter = {}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.LEAD__ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)

    @classmethod
    def search_controller(cls, data):
        query = ''
        if data.get(constants.LEAD__PHONE_NUMBER):
            queryset = cls.db_read_records(read_filter={constants.LEAD__PHONE_NUMBER+"__in": [data.get(constants.LEAD__PHONE_NUMBER)]})
            query = data.get(constants.LEAD__PHONE_NUMBER)
        if data.get(constants.LEAD__ID):
            queryset = cls.db_read_records(read_filter={constants.LEAD__ID: data.get(constants.LEAD__ID)})
            query = data.get(constants.LEAD__ID)
        all_users = []
        users= UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        for id in users:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        if queryset:
            lead = [obj.display_min() for obj in queryset]
            response = {
                'query': data,
                'all_users': all_users,
                'lead':lead[0]
            }
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=response
            )
        else:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.LEAD.title(), query
                ))
    
    @classmethod
    def read_lead_min(cls, data):
        queryset = cls.db_read_records(read_filter={constants.ID+"__in": data})
        temp = [obj.display_min() for obj in queryset]
        return temp

    @classmethod
    def read_lead(cls, data):
        queryset = cls.db_read_records(read_filter={constants.ID+"__in": data})
        temp = [obj.display_transfer() for obj in queryset]
        return temp

    @classmethod
    def bulk_transfer(cls, data):
        from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
        queryset = cls.db_read_records(read_filter={constants.LEAD__ASSIGNED_TO: data['assigned_to']}).limit(int(data['count']))
        
        followup_data_new = {constants.FOLLOW_UP__COMMENT: 'LEAD TRANSFER', 
            constants.FOLLOW_UP__COMPLETION_DATE: datetime.now().strftime(config.DATETIME_FORMAT), constants.FOLLOW_UP__NEXT_DEADLINE: datetime.now().strftime(config.DATETIME_FORMAT),
            constants.FOLLOW_UP__LEVEL: constants.FOLLOW_UP__LEVEL__LIST[2], constants.FOLLOW_UP__TYPE: 'Call', 
            constants.FOLLOW_UP__SUB_TYPE: 'Call_attempt', constants.FOLLOW_UP__NEXT_TASK: 'ContactClient', constants.FOLLOW_UP__STATUS: 'Interested'}
        for lead in queryset:
            update_filter = {constants.ID: lead[constants.ID], constants.LEAD__ASSIGNED_TO: data['transfer_to'], 
            constants.LEAD__ASSIGNED_BY: common_utils.current_user(), constants.LEAD__TRANSFERED: True}
            res = LeadsController.update_controller(update_filter)

            followup = FollowUpController.read_lead_follow(data = {'lead':str(lead[constants.ID])})
            for follow in followup['response_data']:
                followup_updatedata = {constants.FOLLOW_UP__ASSIGNED_TO: data['transfer_to'],
                  constants.ID: follow[constants.ID]}
                res = FollowUpController.update_controller(followup_updatedata)
                
            followup_data_new[constants.FOLLOW_UP__LEAD] = lead[constants.ID]
            followup_data_new[constants.FOLLOW_UP__ASSIGNED_TO] = data['transfer_to']
            res = FollowUpController.create_controller(data=followup_data_new)
        return data

    @classmethod
    def lead_transfer(cls, data):
        from ppBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
        lead_ids = data['lead'].replace('[', '')
        lead_ids = lead_ids.replace(']', '')
        lead_ids = lead_ids.replace('"', '')
        lead_ids = lead_ids.split(',')
        user_childs= UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]

        queryset = LeadsController.read_lead(lead_ids)
        for lead in queryset:
            lead['lead_id'] = lead['id']
            del lead["id"]
            print(lead["assigned_to"].fetch().id)
            if lead["assigned_to"].fetch().id in user_ids:
                res = LeadsHistoryController.create_controller(lead)
                followup = FollowUpController.read_lead_follow(data = {'lead':lead['lead_id'], 'name':'', 'ref':''})
                for follow in followup['response_data'][0]:
                    followup_updatedata = {constants.FOLLOW_UP__ASSIGNED_TO: data['transfer_to'],
                    constants.ID: follow[constants.ID]}
                    res = FollowUpController.update_controller(followup_updatedata)
                leads = {}
                if data['type'] != '':
                    followup_data_new = {constants.FOLLOW_UP__COMMENT: data['comment'], 
                    constants.FOLLOW_UP__COMPLETION_DATE: datetime.now().strftime(config.DATETIME_FORMAT), constants.FOLLOW_UP__NEXT_DEADLINE: data['next_deadline'],
                    constants.FOLLOW_UP__LEVEL: data['lead_level'], constants.FOLLOW_UP__TYPE: data['type'], constants.FOLLOW_UP__ASSIGNED_TO: data['transfer_to'], 
                    constants.FOLLOW_UP__SUB_TYPE: data['sub_type'], constants.FOLLOW_UP__NEXT_TASK: data['next_task'], constants.FOLLOW_UP__STATUS: data['lead_status']}
                    followup_data_new[constants.FOLLOW_UP__LEAD] = lead['lead_id']
                    res = FollowUpController.create_controller(data=followup_data_new)

                    leads[constants.LEAD__FOLLOWUP] = res['response_data'][constants.ID]
                    leads[constants.ID] = res['response_data'][constants.FOLLOW_UP__LEAD]['id']
                    leads[constants.LEAD__COMMENT] = res['response_data'][constants.FOLLOW_UP__COMMENT]
                    leads[constants.LEAD__LEVEL] = res['response_data'][constants.FOLLOW_UP__LEVEL]
                    leads[constants.LEAD__LAST_WORK] = res['response_data']['sub_type']
                    leads[constants.LEAD__LAST_WORK_DATE] = res['response_data']['created_on']
                    leads[constants.LEAD__FOLLOWUP_TYPE] = res['response_data']['type']
                    leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = res['response_data']['next_deadline']
                    leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = res['response_data']['next_task']
                    
                leads[constants.LEAD__ASSIGNED_TO] = data['transfer_to']
                leads[constants.LEAD__ASSIGNED_BY] = common_utils.current_user()
                leads[constants.LEAD__TRANSFERED] = True
                leads[constants.LEAD__TRANSFERED_ON] = common_utils.get_time()  
                res = LeadsController.db_update_single_record(read_filter = {constants.ID:res['response_data'][constants.FOLLOW_UP__LEAD]['id']}, update_filter = leads)
            else:
                return response_utils.get_json_response_object(
                    response_code=response_codes.CODE_LEAD_OUT_OF_BOUND,
                    response_message=response_codes.MESSAGE_INVALID_LEAD
                )
        return response_utils.get_json_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=data
            )
    
    @classmethod
    def lead_bulk_add(cls, data):
        datafile = pd.read_csv(data)
        jout = datafile.to_dict(orient="split")
        unique = []
        duplicates = []
        lead = {}
        for item in jout['data']:
            if item[2] == item[2]:
                # item[2] = item[2].replace(".", "")
                # item[2] = item[2].replace(" ", "")
                # item[2] = re.sub('^00', '+', item[2])
                # item[2] = re.sub('^03', '+923', item[2])
                # item[2] = re.sub('^3', '+923', item[2])
                queryset = cls.db_read_records(read_filter={constants.LEAD__PHONE_NUMBER: item[2]})
                if queryset:
                    duplicates.append(item)
                else:
                    unique.append(item)
                    for index, header in enumerate(jout["columns"]):
                        lead[header] = item[index]       
        if unique:
            pass

        print(jout)