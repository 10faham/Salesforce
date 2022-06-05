db.follow_up.updateMany({},[
{$set:{"assigned_to":"$created_by"}}])

db.leads.updateMany({},
{$unset:{assigned_to:""}})

db.leads.updateMany({},[
{$set:{"assigned_to":"$created_by", "transfered":false}}])


{assigned_to:{$in:[ObjectId('619b5af5a30ed6b97330addf'),ObjectId('619b5d27360643a46baf3818'),ObjectId('619b5e04360643a46baf381b'),ObjectId('619b5e56360643a46baf381c'),ObjectId('619b77b002ce66223367ac36'),ObjectId('619dd021945a75460afc2213'),ObjectId('619dd065945a75460afc2214'),ObjectId('624173f47fec343c6b2cc511'),ObjectId('624174b57fec343c6b2cc512'),ObjectId('6242eec3e92df56342b07716'),ObjectId('6242fab2784f3523a9d820dc'),ObjectId('6253cce240d74a484aff4cd9'),ObjectId('625d0a1721fca4f526e4ad88')]}}


