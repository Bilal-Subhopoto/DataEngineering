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

MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB

StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)#stateDB
#DB11 = redis.Redis(host = '43.251.253.107', port= 1500, db= 11)#for error links
globalPostIDstate = redis.Redis(host = '43.251.253.107', port= 1500, db= 8)#all the seen postIDs

def searchURLinText(postText,FB_key):    
    extractor = URLExtract()
    urls = extractor.find_urls(postText)
    # urls = str(urls)
    for url in urls:     
        url = tldextract.extract(url)
        link = tldextract.extract(FB_key)
        # print("searchURLinText "+url.domain+"  -  "+link.domain)

        if url.domain == link.domain:
            return True
            break
    return False
def searchURL(postLink,FB_key):
    URL = tldextract.extract(postLink)
    links = tldextract.extract(FB_key)
    # print("searchURL "+URL.domain +"  -  "+links.domain)

    if URL.domain == links.domain:
        return True
    else:
        return False


def FBscraper(PAGES,FB):

    pgs = 0
    # fb urls to extract posts data and upload on DB-1
    fields = ('comments','link','likes','images','shared_time','text','post_id','reactions','shares','user_id','time','timestamp','time')
    inPageDelayslist = [1,2,3] 
        
   
       

        
    try:
        myclient = pymongo.MongoClient("mongodb://43.251.253.107:1600/")
        mydb = myclient['FB_scraper_MT4']
        mycol = mydb['Allposts']
        ud_fbp_Key = StateDB.srandmember('allurls')
        fbp_Key = ud_fbp_Key.decode('utf-8')
        value = MasterDB.srandmember(fbp_Key)#
        Dvalue = value.decode('utf-8')
        fbp = Dvalue.split('||')[0]
        
    except Exception as e:
        print('decoding error :', e)
        #DB11.sadd('D '+fbp_Key,value)
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
                   
                    
                    # print(fbp+"  -  "+str(post['post_id']))
                    
                    time.sleep(random.choice(inPostDelayslist))
                    collection = {'DomainName':fbp_Key, 'pageName':fbp}#add a column of website name  and add a column of FB pagename        
                    
                    for items in fields:

                        collection[items] = (post[items])
                    from datetime import datetime
                    collection["TimeDownload"] = datetime.now()  
                    
                    

                    globalStateinserted = globalPostIDstate.sadd(fbp,collection["post_id"])#fbp = post["pageName"] here

                    urlfoundinText=False
                    # urlfoundinText = searchURLinText(post["text"],fbp_Key)#fbp_key = post["DomainName"]
                    urlfound=False
                    if post["link"] is not None:
                        urlfound = searchURL(post["link"],fbp_Key)#fbp_key = post["DomainName"]
                    else:
                        print("post['link]  is empty")    
                    print("urlfoundinText: "+str(urlfoundinText))
                    print("urlfound: "+str(urlfound))
                    if urlfoundinText or urlfound:
                        logger.info(get_colors('000128000', 'BackWhite') + 'Link Found in post!' )

                        print(post["link"])
                        # print(post["text"])
                        print("+++++++++++++++++++++++++++++++++++++++++")
                #00efeb

                        if globalStateinserted == 0:#in case the post exists in global... 
                            countglobalStateinserted +=1
                            logger.info(get_colors('#ef4c00', 'BackWhite') + 'Link already exists in state redis '+str(countglobalStateinserted) )

                            



                        from datetime import datetime
                        # if post["time"] is not None:post["time"] is never null/for loop through all the MT2 database and check if "time" is empty in any doc.
                        if post["time"].date()<datetime.now().date()  or countglobalStateinserted == 3:
                            if countglobalStateinserted == 3:
                                logger.info(get_colors('#030102', 'BackWhite') + 'Breaking loop after 3 times link found in state'+str(countglobalStateinserted) )
                            else:
                                print(post["time"].date())
                                print(datetime.now().date())
                                logger.info(get_colors('#030102', 'BackWhite') + 'Breaking loop after seeing old post '+str(countglobalStateinserted) )
                            break
                        else:

                            mycol.insert_one(collection)
                            logger.info(get_colors('#ef4c00', 'BackWhite') + 'Inserted in mongo ' )



                            
                            
        
            
                    else:
                        logger.info(get_colors('red', 'BackWhite') + 'Link not found in post ignoring the post:')
                        print(post["link"])
                        # print(post["text"])
                        print("------------------------------------------------------")
                    logger.info(get_colors('#008888') + 'next!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')   


                print("All done: "+str(psts))
                
                keyRemoved=StateDB.srem('allurls',fbp_Key)
                print(">>>>>>>>>>>>>>> key removed "+str(fbp_Key)+"  -  "+str(keyRemoved))
                
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
        
    
    fbpCount = len(StateDB.smembers("allurls"))
        
    
    return fbpCount
    # print('number of posts per page: ',psts)
    # pgs +=1#increment page count
    # print('number of FB pages scraped: ', pgs)
    # if (pgs == 5):
    #     break




def basic_func(x):

       
    # count=0 #initialize counter for number of pages scraped to jump to change cookies file and continue scraping.
    
    try:
        FB = FacebookScraper()
        FB.set_proxy("http://192.151.150.174:2000")
    except Exception as e:
        print(e)

    while(1):
        
        count = FBscraper(5,FB)
         
        print("number of FB pages remaining in stateDB: ",count,"#######################")
        print("number of FB pages remaining in stateDB: ",count,"#######################")
        print("number of FB pages remaining in stateDB: ",count,"#######################")
        if count < 10:
            etime = datetime.now()
            ttime = etime - stime
            total_seconds = ttime.total_seconds()
            minutes = total_seconds/60
            print("minutes taken to scraper : ", minutes)
            print("minutes taken to scraper : ", minutes)
            print("minutes taken to scraper : ", minutes)




process=[0,1,2,3,4,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,6,7,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
def multiprocessing_func(x):
    basic_func(x)
    
   
# if name == '__main__':
    
starttime = time.time()
pool = Pool(processes=13)              # start 4 worker processes
pool.map(multiprocessing_func, process)
pool.close
