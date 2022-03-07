from telnetlib import theNULL
from turtle import pos
from pymongo import MongoClient
from TestTablemain import TestTable,session
import time
from datetime import datetime,date
from log21 import get_logger, get_colors

logger = get_logger("LOG21", show_time=False)


start = datetime.now()
start1 = start.strftime("%m/%d/%Y, %H:%M:%S")
logger.info(get_colors('#ef4c00', 'BackWhite') + start1)

def CopyFromColl1ToColl2(database1,collection1):
    nonenull = 0
    null = 0
    db1 = MongoClient('mongodb://43.251.253.107:1600/')[database1][collection1]
    
    #here you can put the filters you like.
    
    for a in db1.find():
        
        try:
            
            
            
            if (a['domain']!=None) & (a['pageName']!=None) & (a['user_id']!=None) & (a['post_id']!=None) & (a["dateDownload"]!=None):
                logger.info(get_colors('#ef4c00', 'BackWhite') +str(nonenull)+" Documents inserted")
                logger.info(get_colors('#ef4c00', 'BackWhite') +str(null)+" Erroneous documents")
                
                
                nonenull+=1
                # domain_name=Column(TEXT(),nullable=False)
                # page_name=Column(TEXT(),nullable=False)
                # user_id=Column(TEXT(),nullable=False)
                # date_download=Column(DATE(),nullable=False)
                # post_text =Column(TEXT())#this should be unique and on conflict do nothing, in that case foreign key will have to be searched for by table entry, not immediately after insert into
                # post_id=Column(TEXT(),nullable=False)
                # link=Column(TEXT())
                # post_likes=Column(Integer())
                # post_shares=Column(Integer())

                new_entry=TestTable(
                    date_download = a['dateDownload'],
                    post_likes = a['likes'],
                    post_shares = a['shares'],
                    domain_name=a['domain'],
                    page_name = a['pageName'],
                    user_id = a['user_id'],                    
                    post_id = a['post_id'],
                    post_text = a['text'],                    
                    link = a['link']
                    
                )
                session.add(new_entry)

                session.commit()

                session.flush()
        

                session.refresh(new_entry)

                print(new_entry.id)
                print("#########################################")
                print(new_entry)
                
            else:
                null+=1
                
                logger.info(get_colors('#ef4c00', 'BackWhite') +"else body start#############")
                logger.info(get_colors('#ef4c00', 'BackWhite') +str(nonenull)+" Documents inserted")
                logger.info(get_colors('#ef4c00', 'BackWhite') +str(null)+" Erroneous documents")    
                print(a['domain'])
                print(a['pageName'])
                print(a['user_id'])
                print(a['post_id'])
                print(a["dateDownload"])
                logger.info(get_colors('#ef4c00', 'BackWhite') +"else body end###############")
                time.sleep(8)
        except Exception as e:
            logger.info(get_colors('#ef4c00', 'BackWhite') +str(nonenull)+" Documents inserted")
            logger.info(get_colors('#ef4c00', 'BackWhite') +str(null)+" Erroneous documents")
            print(e)
            break
    logger.info(get_colors('#ef4c00', 'BackWhite') +str(db1.count_documents({}))+" Total documents in mongoDB")
    

# You can choose the database name and the collection name
CopyFromColl1ToColl2('Staging_Synthetic_DB','Allposts')
print("\n")
end = datetime.now()
end1 = end.strftime("%m/%d/%Y, %H:%M:%S")
timee = end - start
logger.info(get_colors('#ef4c00', 'BackWhite') +end1)
logger.info(get_colors('#ef4c00', 'BackWhite') +"total time taken: "+str(timee))






