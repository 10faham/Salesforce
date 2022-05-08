db.leads.updateMany({},[
{$set:{"assigned_to":"$created_by"}}])

db.leads.updateMany({},
{$unset:{assigned_to:""}})