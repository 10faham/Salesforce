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
            'followup_id': {
                '$last': {'$toString': '$_id'}
            }, 
            'followup_follow_id': {
                '$last': '$follow_id'
            }, 
            'followup_sub_type': {
                '$last': '$sub_type'
            }, 
            'followup_completion_date': {
                '$last': '$completion_date'
            }, 
            'followup_comment': {
                '$last': '$comment'
            }
        }
    }
]
