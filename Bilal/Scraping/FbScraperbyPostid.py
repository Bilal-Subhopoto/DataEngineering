from asyncio import exceptions
from itertools import count
from logging import exception
from facebook_scraper import*
import time
from datetime import date, datetime
import random


import time

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

#try to bring it close to a function so that we can later use it as a function with postids

stime = datetime.now()
globalPostIDstate = redis.Redis(host = '43.251.253.107', port= 1500, db= 8)#all the seen postIDs




def FBscraper(post_id_list,FB,fbp_Key,fbp):

    pgs = 0
    # fb urls to extract posts data and upload on DB-1
    fields = ('comments','link','likes','images','shared_time','text','post_id','reactions','shares','user_id','time','timestamp','time','post_url')
    inPageDelayslist = [1,2,3] 
        
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
            print(countBlocks)
            try:
            
                for post in FB.get_posts(fbp, post_urls = post_id_list, start_url=start_url, request_url_callback=handle_pagination_url):
                   
                    
                    print(fbp+"  -  "+str(post['post_url']))
                    if str(post['post_url']) == post_id_list:
                        print("post id works########################### post url: ", post['post_url'])
                        time.sleep(random.choice(inPostDelayslist))
                        collection = {'DomainName':fbp_Key, 'pageName':fbp}#add a column of website name  and add a column of FB pagename        
                        
                        for items in fields:

                            collection[items] = (post[items])
                            print("post id works########## ",items, " ",collection[items])
                        from datetime import datetime
                        collection["TimeDownload"] = datetime.now()  
                    
                    
                    

                    
                print("All done: "+str(psts))
                
                
                
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
      
        
    
id_list = ["4721091164633785"]#["4726902150731909"]#,"",
        # "462945805456709","10159910571379245",
        # "3459954204044235"]

fbpages ={"theforwardcabin.com":"theforwardcabin"}#,
        #{"jagoinvestor.com":"Jagoinvestor.blog"}#,
        # "mszgnews.com":"mszgnews",
        # "crazyleafdesign.com":"crazyleafdesign",
        # "theultralinx.com":"UltraLinx"}


i = 0
for fbp_key in fbpages:
    
    try:
        FB = FacebookScraper()
        # FB.set_proxy("http://192.151.150.174:2000")
        
    except Exception as e:
        print(e)
    FBscraper("https://www.facebook.com/story.php?story_fbid=2257188721032235&id=119240841493711",FB,fbp_key,"Nintendo")#fbp =fbpages[fbp_key]
    # print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    # globalPostID = globalPostIDstate.srandmember(fbpages[fbp_key])#get a post id under fbp from above list(fbpages)
    # globalPostID = globalPostID.decode('utf-8')
    # print(globalPostID)
    # FBscraper(globalPostID,FB,fbp_key,fbpages[fbp_key])#fbp =fbpages[fbp_key]
    # print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    i+=1