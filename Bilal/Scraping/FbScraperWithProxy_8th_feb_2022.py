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
import datetime
import random
from multiprocessing import Pool
import redis
from urlextract import URLExtract




MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB

StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)#stateDB
DB11 = redis.Redis(host = '43.251.253.107', port= 1500, db= 11)#for error links
globalPostIDstate = redis.Redis(host = '43.251.253.107', port= 1500, db= 8)#all the seen postIDs



def FBscraper(PAGES,FB):

    pgs = 0
    # fb urls to extract posts data and upload on DB-1
    fields = ('comments','link','likes','images','shared_time','text','post_id','reactions','shares','user_id','time','timestamp','time')
    inPageDelayslist = [1,2,3] 
        
   
       

        
    try:
        myclient = pymongo.MongoClient("mongodb://43.251.253.107:1600/")
        mydb = myclient['FB_scraper_MT3']
        mycol = mydb['Allposts']
        ud_fbp_Key = StateDB.srandmember('allurls')
        fbp_Key = ud_fbp_Key.decode('utf-8')
        value = MasterDB.srandmember(fbp_Key)#
        Dvalue = value.decode('utf-8')
        fbp = Dvalue.split('||')[0]
    except Exception as e:
        print('decoding error :', e)
        DB11.sadd('D '+fbp_Key,value)
        StateDB.srem('allurls',fbp_Key)
        
    time.sleep(random.choice(inPageDelayslist))
    # print(fbp)
    psts = 0    
    inPostDelayslist = [1,2,3,4] 
    try:
        FB = FacebookScraper()
        FB.set_proxy("http://192.151.150.174:2000")
    except Exception as e:
        print(e)   
    try:
        results = []
        start_url = None
        def handle_pagination_url(url):
            global start_url
            start_url = url


        countBlocks = 0
        while countBlocks<=5:
            countBlocks+=1
            try:
                countglobalStateinserted = 0
                for post in FB.get_posts(fbp, pages= PAGES, start_url=start_url, request_url_callback=handle_pagination_url):
                    # print("\n\n\n#####################################################################################")
                    # print(post["time"].date())
                    # from datetime import datetime
                    # print(datetime.now().date())
                    
                    print(fbp+"  -  "+str(post['post_id']))
                    # print("#####################################################################################\n\n\n")
                    time.sleep(random.choice(inPostDelayslist))
                    collection = {'DomainName':fbp_Key, 'pageName':fbp}#add a column of website name  and add a column of FB pagename        

                    for items in fields:
                        collection[items] = (post[items])

                    collection["TimeDownload"] =datetime.datetime.now()   
                                        
                    globalStateinserted = globalPostIDstate.sadd(fbp,post['post_id'])#check if the post already exists
                    urlfoundinText = searchURLinText(post["text"],fbp_Key)
                    urlfound = searchURL(post["link"],fbp_Key)

                    
                    if (globalPostIDstate == 1):
                        if urlfoundinText or urlfound:
                            x = mycol.insert_one(collection)
                    if globalStateinserted == 0:#in case the post exists in global... 
                        countglobalStateinserted +=1
                    
                    print(post["time"],"post////////////////")
                    print(collection["time"],"collection////////////////")
                    psts +=1 #increment posts count
                    from datetime import datetime
                    # if post["time"] is not None:post["time"] is never null/for loop through all the MT2 database and check if "time" is empty in any doc.
                    if post["time"].date()<datetime.now().date():#(check if (post post["time"].date is less than datetime.now().date) or (countglobalStateinserted == 3):
                        print("\n\n\n#####################################################################################")
                        print(post["time"].date())
                        print(datetime.now().date())
                        print("#####################################################################################\n\n\n")
                        break
                    if countglobalStateinserted == 3:
                        print("#####################################################################################")
                        print("count = 3")
                        break
                        
                print("All done: "+str(psts))
                StateDB.srem('allurls',fbp_Key)

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
        DB11.sadd('U '+fbp_Key,value)
        return
        # StateDB.srem('allurls',fbp_Key)
        
    
    # print('number of posts per page: ',psts)
    # pgs +=1#increment page count
    # print('number of FB pages scraped: ', pgs)
    # if (pgs == 5):
    #     break
def searchURLinText(text,domain):
    

    extractor = URLExtract()
    urls = extractor.find_urls(text)
    print(urls) # prints: ['janlipovsky.cz']
    if urls.domain == domain:
        return True
    else:
        return False
def searchURL(url,domain):
    
    if url.domain == domain:
        return True
    else:
        return False

def basic_func(x):

       
    count=0 #initialize counter for number of pages scraped to jump to change cookies file and continue scraping.
    try:
        FB = FacebookScraper()
        FB.set_proxy("http://192.151.150.174:2000")
    except Exception as e:
        print(e)

    while(1):
        FBscraper(5,FB)
        count+=1





# StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)#stateDB

# MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB


# StateDB.flushdb()
# #copy only keys
# MDB_keys=MasterDB.keys()    

# for keyM in MDB_keys:
#     dkey = keyM.decode("utf-8")
    
#     StateDB.sadd('allurls',dkey)

# basic_func(1)


process=[0,1,2,3,4,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
def multiprocessing_func(x):
    basic_func(x)
    
   
# if name == '__main__':
    
starttime = time.time()
pool = Pool(processes=130)              # start 4 worker processes
pool.map(multiprocessing_func, process)
pool.close
