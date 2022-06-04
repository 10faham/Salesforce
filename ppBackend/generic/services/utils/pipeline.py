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
            '_id': '$lead', 
            'follow_count': {
                '$sum': 1
            }, 
            'id': {
                '$last': {
                    '$toString': '$_id'
                }
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
            }, 
            'project': {
                '$last': '$next_project'
            }
        }
    }, {
        '$lookup': {
            'from': 'leads', 
            'localField': '_id', 
            'foreignField': '_id', 
            'pipeline': [
                {
                    '$addFields': {
                        '_id': {
                            '$toString': '$_id'
                        }, 
                        'created_by': {
                            '$toString': '$created_by'
                        }
                    }
                }
            ], 
            'as': 'lead'
        }
    }, {
        '$lookup': {
            'from': 'user', 
            'localField': 'lead.assigned_to', 
            'foreignField': '_id', 
            'as': 'user'
        }
    }, {
        '$project': {
            'follow_count': 1, 
            'id': {
                '$toString': '$id'
            }, 
            '_id': {
                '$toString': '$_id'
            }, 
            'follow_id': 1, 
            'sub_type': 1, 
            'completion_date': 1, 
            'comment': 1, 
            'next_task': 1, 
            'deadline': 1, 
            'created_on': 1, 
            'lead.first_name': 1, 
            'lead.phone_number': 1, 
            'lead.lead_id': 1, 
            'user.name': 1, 
            'project': 1
        }
    }, {
        '$addFields': {
            'user': {
                '$arrayElemAt': [
                    '$user', 0
                ]
            }, 
            'lead': {
                '$arrayElemAt': [
                    '$lead', 0
                ]
            }
        }
    }
]

ALL_LEADS = [
    {
        '$sort': {
            '_id': -1
        }
    }, {
        '$lookup': {
            'from': 'follow_up', 
            'localField': '_id', 
            'foreignField': 'lead', 
            'pipeline': [
                {
                    '$group': {
                        '_id': {
                            '$toString': '$lead'
                        }, 
                        'follow_count': {
                            '$sum': 1
                        }, 
                        'id': {
                            '$last': {
                                '$toString': '$_id'
                            }
                        }, 
                        'follow_id': {
                            '$last': '$follow_id'
                        }, 
                        'sub_type': {
                            '$last': '$sub_type'
                        }, 
                        'comment': {
                            '$last': '$comment'
                        }, 
                        'created_on': {
                            '$last': {
                                '$toDate': '$created_on'
                            }
                        }
                    }
                }
            ], 
            'as': 'followup'
        }
    }, {
        '$lookup': {
            'from': 'user', 
            'localField': 'assigned_to', 
            'foreignField': '_id', 
            'as': 'user'
        }
    }, {
        '$project': {
            '_id': {
                '$toString': '$_id'
            }, 
            'created_on': {
                '$toDate': '$created_on'
            }, 
            'first_name': 1, 
            'phone_number': 1, 
            'project': 1, 
            'lead_level': 1, 
            'lead_id': 1, 
            'followup.id': 1, 
            'followup.follow_id': 1, 
            'followup.sub_type': 1, 
            'followup.comment': 1, 
            'followup.created_on': 1, 
            'followup.follow_count': 1, 
            'user.name': 1
        }
    }, {
        '$addFields': {
            'user': {
                '$arrayElemAt': [
                    '$user', 0
                ]
            }, 
            'followup': {
                '$arrayElemAt': [
                    '$followup', 0
                ]
            }, 
            'created_on': {
                '$substrBytes': [
                    '$created_on', 0, 10
                ]
            }
        }
    }, {
        '$addFields': {
            'followup.created_on': {
                '$substrBytes': [
                    '$followup.created_on', 0, 10
                ]
            }
        }
    }
]