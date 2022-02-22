from asyncio import exceptions
from itertools import count
from logging import exception
from facebook_scraper import*
import time
from datetime import date, datetime
import random
import pymongo
import redis

import time
import multiprocessing 
import multiprocessing 
import json
import os
import time
import sys
from datetime import datetime
import random
from multiprocessing import Pool
import redis
from urlextract import URLExtract
import tldextract
from log21 import get_logger, get_colors

logger = get_logger("LOG21", show_time=False)



stime = datetime.now()

MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 9)#id :domainname||pagename

StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 11)#stateDB = allpostids:idssss
# psts = 0


def FBscraper(FB,postid,dom,fbp):
    pgs = 0
    # fb urls to extract posts data and upload on DB-1
    fields = ('comments','link','likes','images','shared_time','text','post_id','reactions','shares','user_id','time','timestamp','time')
    inPageDelayslist = [1,2,3] 
        
   
       

        
    
    myclient = pymongo.MongoClient("mongodb://43.251.253.107:1600/")
    mydb = myclient['FB_scraper_MT5']
    mycol = mydb['Allposts']
    time.sleep(random.choice(inPageDelayslist))
    # print(fbp)
     
    inPostDelayslist = [1,2,3,4] 
    try:
        FB = FacebookScraper()
        FB.set_proxy("http://192.151.150.174:2000")
    except Exception as e:
        print(e)   
    try:
        # results = []
        # start_url = None
        # def handle_pagination_url(url):
        #     global start_url
        #     start_url = url


        countBlocks = 0
        psts = 0
        while countBlocks<=10:
            countBlocks+=1
           
            try:
                print("at START     "+postid )
                post = next(get_posts(post_urls=[postid]))
                post['post_url'][:1000]
                # collection['text']= post['text'][:1000]
                # collection = {'DomainName':dom, 'pageName':fbp}#add a column of website name and add a column of FB pagename                
                # from datetime import datetime
                # collection["TimeDownload"] = datetime.now()
                print("All done: "+str(psts))

                mycol.insert_one(collection)
                logger.info(get_colors('#ef4c00', 'BackWhite') + 'Inserted in mongo ' )
                          
                        
                # for post in FB.get_posts(fbp, post_urls = postid, start_url=start_url, request_url_callback=handle_pagination_url):
                    
                #     if psts == 3:
                #         logger.info(get_colors('#008888', 'BackWhite') + 'Three posts scraped')  
                #         break
                #     # print(fbp+"  -  "+str(post['post_id']))
                #     if post['post_id'] == postid:
                #         time.sleep(random.choice(inPostDelayslist))
                        
                #         collection = {'DomainName':dom, 'pageName':fbp}#add a column of website name and add a column of FB pagename        
                        
                #         for items in fields:

                #             collection[items] = (post[items])
                        
                #         psts+=1
                #         from datetime import datetime
                #         collection["TimeDownload"] = datetime.now()  
                        
                        

                        # logger.info(get_colors('#008888', 'BackWhite') + 'Collection: ',collection)
                        # mycol.insert_one(collection)
                        # logger.info(get_colors('#ef4c00', 'BackWhite') + 'Inserted in mongo ' )
                    # logger.info(get_colors('#00efef', 'BackWhite') + 'Total posts scraped: ',psts)
                    
                # print("All done: "+str(psts))
                
                keyRemoved=StateDB.srem('allpostids',postid)
                logger.info(get_colors('#ef4c00', 'BackWhite') + 'removing key' )
                print(">>>>>>>>>>>>>>> key removed "+str(postid)+"  -  "+str(keyRemoved))
                
                break

            except Exception as e:

                print('in loop Error :', str(e))
                try:
                    FB = FacebookScraper()
                    FB.set_proxy("http://192.151.150.174:2000")
                except Exception as e:
                    print(e)   


    except Exception as e:
        print('Outer Try Error :', str(e))
        #DB11.sadd('U '+fbp_Key,value)
        
        # StateDB.srem('allurls',fbp_Key)
        
    
    fbpCount = len(StateDB.smembers("allpostids"))
        
    
    return fbpCount




def basic_func(x):       
    
        
    # count=0 #initialize counter for number of pages scraped to jump to change cookies file and continue scraping.
    
    try:
        FB = FacebookScraper()
        FB.set_proxy("http://192.151.150.174:2000")
    except Exception as e:
        print(e)

    while(1):
        try:
        
            ud_fbp_Key = StateDB.srandmember('allpostids')
            postID = ud_fbp_Key.decode('utf-8')#postid
            value = MasterDB.srandmember(postID)
            Dvalue = value.decode('utf-8')#domainname||pagename
            DOM = Dvalue.split('||')[0]#domainname
            FBP = Dvalue.split('||')[1]#pagename
        
        
        except Exception as e:
            print('decoding error :', e)
            
            # StateDB.srem('allpostids',postID)#remove postid from allpostids
        
        count = FBscraper(FB,postID,DOM,FBP)
         
        print("number of FB pages remaining in stateDB: ",count,"#######################")
        print("number of FB pages remaining in stateDB: ",count,"#######################")
        print("number of FB pages remaining in stateDB: ",count,"#######################")
        etime = datetime.now()
        ttime = etime - stime
        total_seconds = ttime.total_seconds()
        minutes = total_seconds/60
        print(2326-count," Post_ids used in: ", minutes," minutes")
        print(2326-count," Post_ids used in: ", minutes," minutes")
        print(2326-count," Post_ids used in: ", minutes," minutes")
        if count < 10:
            etime = datetime.now()
            ttime = etime - stime
            total_seconds = ttime.total_seconds()
            minutes = total_seconds/60
            print(2326-count," Post_ids used in: ", minutes," minutes")
            print(2326-count," Post_ids used in: ", minutes," minutes")
            print(2326-count," Post_ids used in: ", minutes," minutes")




process=[0,1,2,3,4,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
def multiprocessing_func(x):
    basic_func(x)
    
   
# if name == '__main__':
    
starttime = time.time()
pool = Pool(processes=13)              # start 4 worker processes
pool.map(multiprocessing_func, process)
pool.close
