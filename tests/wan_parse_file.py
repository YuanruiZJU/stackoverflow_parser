import pymongo
import datetime
# parse XML dataset
from lxml import etree
# parse tags
import re

## connect to mongodb
db = pymongo.MongoClient().stackoverflow
coll = db.blockchain

## path to Posts.xml
path = '/media/zhiyuan/Samsung_T3/stackoverflow.com-Posts/'
input_file = path + 'Posts.xml'

# Parse XML file
finished_id = 0
skipped = 0

context = etree.iterparse(input_file, events=('end',), tag='row')
for event, row in context:
    if event == 'end' and row.tag == 'row':
        post_id = row.get('Id')

        ## In case the process is interrupted
        if finished_id > int(post_id):
            skipped += 1
            if skipped % 50000 == 0:
                print("Skipped 50000, now at " + post_id)
            row.clear()
            continue

        ## extract info from XML
        type_id = row.get('PostTypeId')
        creation_date = row.get('CreationDate')
        score = row.get('Score')
        view_count = row.get('ViewCount')
        body = row.get('Body')
        title = row.get('Title')

        post = {
            "Id": post_id,
            "PostTypeId": type_id,
            "CreationDate": datetime.datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S.%f"),
            "Score": score,
            "ViewCount": view_count,
            "Body": body,
            "Title": title,
            "Tags": tag_vec,
        }

        # Insert into collection
        coll.insert(post)
        row.clear()
