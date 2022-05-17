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
