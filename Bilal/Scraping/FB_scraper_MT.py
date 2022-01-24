from asyncio import exceptions
from logging import exception
from facebook_scraper import*
import time
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
from feedsearch_crawler import search
import redis




MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB

StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)#stateDB
DB11 = redis.Redis(host = '43.251.253.107', port= 1500, db= 11)#for error links 



def FBscraper(PAGES,COOKIES):
# get keys of MasterDB
    # allurlsValues = StateDB.smembers('allurls')   

  
    pgs = 0
    # fb urls to extract posts data and upload on DB-1
    fields = ('comments','link','likes','images','shared_time','text','post_id','reactions','shares','user_id','time','timestamp','time')
    inPageDelayslist = [10,22,8,12,15,40,7,20,15,30]
    # allurlsValues = ('ABCNews','cnn','NBCNews','mlive','TheIndependentOnline','thedailybeast','WashingtonExaminer','Gawker','Upworthy','chroncom','Slate','bleacherreport','EliteDaily','washingtonpost','DailyMail','nytimes','BuzzFeed','usatoday','CBSNews','HuffPost')
    # for VAL in allurlsValues:
        
    try:
       

        
        try:
            myclient = pymongo.MongoClient("mongodb://43.251.253.107:1600/")
            mydb = myclient['FB_scraper_MT']
            mycol = mydb['Allposts']
            ud_fbp_Key = StateDB.srandmember('allurls')
            fbp_Key = ud_fbp_Key.decode('utf-8')
            print(fbp_Key)
            value = MasterDB.srandmember(fbp_Key)#
            Dvalue = value.decode('utf-8')
            fbp = Dvalue.split('||')[0]
            print(fbp)
        except Exception as e:
            print('decoding error :', e)
            DB11.sadd('D '+fbp_Key,value)
            StateDB.srem('allurls',fbp_Key)
            
        time.sleep(random.choice(inPageDelayslist))
        print(fbp)
        psts = 0    
        inPostDelayslist = [10,5,3,12,3,40,7,5]    
        try:
            for post in get_posts(fbp, pages= PAGES ,cookies= COOKIES):
                collection = {'DomainName':fbp_Key, 'pageName':fbp}#add a column of website name  and add a column of FB pagename        
                time.sleep(random.choice(inPostDelayslist))
                print('testing print')
                for items in fields:
                    collection[items] = (post[items])
                    
                x = mycol.insert_one(collection)
                psts +=1 #increment posts count
                if (psts == 4):
                    break
        except Exception as e:
            print('URL Error :', e)
            DB11.sadd('U '+fbp_Key,value)
            StateDB.srem('allurls',fbp_Key)
            
        
        print('number of posts per page: ',psts)
        pgs +=1#increment page count
        StateDB.srem('allurls',fbp_Key)
        print('number of FB pages scraped: ', pgs)
        # if (pgs == 5):
        #     break
        
    except exceptions.TemporarilyBanned:
        print("Temporarily banned, sleeping for 10m")
        print('number of FB pages scraped before error : ', pgs)
        time.sleep(3600)

def basic_func(x):

        

    cookiesAdd = ['Cookies_BabarAzam.txt','Cookies_IrfanKhan.txt','Cookies_SaifMagsi.txt']

    credentials=cookiesAdd[x]#choose a random cookies file.
    count=0 #initialize counter for number of pages scraped to jump to change cookies file and continue scraping.
    
    while(1):
        
        print('cookies file used: ',credentials)
        # pn=stateDB.srandmember()# key=pagename  : a key or masterdb
        FBscraper(5,credentials)
        count+=1





StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)#stateDB

MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB


StateDB.flushdb()
#copy only keys
MDB_keys=MasterDB.keys()    

for keyM in MDB_keys:
    dkey = keyM.decode("utf-8")
    
    StateDB.sadd('allurls',dkey)



process=[0,1,2]
def multiprocessing_func(x):
    basic_func(x)
    
   
# if name == '__main__':
    
starttime = time.time()
pool = Pool(processes=3)              # start 4 worker processes
pool.map(multiprocessing_func, process)
pool.close
