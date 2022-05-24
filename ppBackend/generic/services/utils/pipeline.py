KPI_REPORT_FOLLOW_UP = [
    {
        '$group': {
            '_id': {
                'created_by': '$created_by',
                'type': '$type',
                'sub_type': '$sub_type'
            },
            'count': {
                '$sum': 1
            }
        }
    },
    {
        "$sort": {"created_by": 1}
    }
]

KPI_REPORT_LEAD_COUNT = [
    {
        '$group': {
            '_id': '$assigned_to',
            "lead_count": {
                "$sum": 1
            }
        }
    }
]

LAST_FOLLOWUP = [
    {
        '$sort': {
            'next_deadline': 1,
            '_id': 1
        }
    }, {
        '$group': {
            '_id': {'$toString':'$lead'}, 
            'follow_count': {
                '$sum': 1
            }, 
            'id': {
                '$last': {'$toString': '$_id'}
            }, 
            'follow_id': {
                '$last': '$follow_id'
            }, 
            'sub_type': {
                '$last': '$sub_type'
            }, 
            'completion_date': {
                '$last': '$completion_date'
            }, 
            'comment': {
                '$last': '$comment'
            },
            'next_task': {
                '$last': '$next_task'
            },
            'deadline': {
                '$last': '$next_deadline'
            },
            'created_on': {
                '$last': '$created_on'
            }

        }
    }
]
