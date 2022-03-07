from turtle import update
from pymongo import MongoClient
from datetime import datetime,date,time
import random
from bson.objectid import ObjectId

from log21 import get_logger, get_colors
from datetime import datetime, timedelta ,date

start = datetime.now()
print(start)
logger = get_logger("LOG21", show_time=False)

def CopyFromColl1ToColl2(database1,collection1,database2,collection2):
    
    db1 = MongoClient('mongodb://43.251.253.107:1600/')[database1][collection1]
    db2 = MongoClient('mongodb://43.251.253.107:1600/')[database2][collection2]
   
    for a in db1.find():
        
        try:
            if (a['domain']!=None) & (a['pageName']!=None) & (a['user_id']!=None) & (a['post_id']!=None) & (a["dateDownload"]!=None):
               
                
                a['_id'] = a['post_id']+"_"+str(a['dateDownload'].date())
                
                try:
                    ins = db2.insert_one(a)
                    # print(ins)
                except Exception as e:
                    print("Inner Exception")
                    gets = db2.find_one({"_id":a['_id']})
                    if int(gets['shares']) < int(a['shares']) or int(gets['likes']) < int(a['likes']):# or gets['comments']>a['comments']:
                        print("\n")
                        print(gets['pageName']+"--"+a['pageName'])
                        print(str(gets['shares'])+"--"+str(a['shares']))
                        print(str(gets['likes'])+"--"+str(a['likes']))
                        print("\n")
                        try:
                            rep = db2.replace_one({"_id" : a['_id']}, a)
                            print("success")
                        except Exception as e:
                            print(e)

        except Exception as e:
            print("Outer Exception",e)
    logger.info(get_colors('#ef4c00', 'BackWhite') + str(db2.count_documents({})))

# You can choose the database name and the collection name
CopyFromColl1ToColl2('Synthetic_FB_Data','Allposts','Staging_Synthetic_DB','Allposts')
print(datetime.now()-start)
