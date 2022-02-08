

import os
import feedparser
import redis
import json
import time
import multiprocessing 
import sys
import datetime
import random
from multiprocessing import Pool
import tldextract
import dateparser

from newsplease import NewsPlease

from newspaper import Article

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from random import randrange
from iso_language_codes import *
# es = Elasticsearch()
# http://192.168.100.85:9200/
es=Elasticsearch(['http://43.251.253.107'],port=1200, timeout=100)
# es=Elasticsearch(['http://192.168.0.109'],port=9200, timeout=100)

masterDB = redis.Redis(host='43.251.253.107', port=1500, db=13)
todayDB = redis.Redis(host='43.251.253.107', port=1500, db=9)
globalUrlsStore = redis.Redis(host='43.251.253.107', port=1500, db=15)

import readtime
import time
import datetime


# from datetime import datetime, timedelta
# yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d %H:%M:%S')
from datetime import datetime, timedelta ,date

yesterday=datetime.strftime(date.today() - timedelta(2), '%Y-%m-%d %H:%M:%S')

print("yesterday :"+yesterday)
datetime_str = '23:50:00'

datetime_object = datetime.strptime(datetime_str, '%H:%M:%S')
thrushHour=datetime_object.hour
print("thrushour : "+str(thrushHour))
rightNow=datetime.now().hour

if rightNow<thrushHour:
# if 2>1:
    print("morning")
    todayDB.flushdb()
    keys=masterDB.keys()   
    listcols=[]
    for key in keys:
    #     print(key.decode("utf-8"))
        # listcols.append()
        todayDB.sadd('allurls',key.decode("utf-8"))

        


    # for d in listcols:
    #     rssFeedUrls= masterDB.smembers(d) 
    #     for feedUrl in rssFeedUrls:
    #         decodedFeedUrl=feedUrl.decode("utf-8") 
    #         todayDB.sadd(d,decodedFeedUrl)
else:
    print("not morning")            


mylist = list(range(200))
# print(mylist)            
# keys=todayDB.keys()   
# todaysDomains=[]
# for key in keys:
# #     print(key.decode("utf-8"))
#     todaysDomains.append(key.decode("utf-8"))
    
# print(len(todaysDomains))

import tldextract






def getFeedUrls(domain):
    allurls=[]
    try:
        rssFeedUrls= masterDB.smembers(domain) 
        # print(rssFeedUrls)
        cleanDomain=domain


        for feedUrl in rssFeedUrls:
            decodedFeedUrl=feedUrl.decode("utf-8")
            
            go =False

            try:
                feed = feedparser.parse(decodedFeedUrl)

                for entry in feed['entries']:
                    # date_time_Captured = dateparser.parse(entry['published'])
                    # date_time_Limit = dateparser.parse(str(yesterday)+"+00:00")

                    # if date_time_Captured>date_time_Limit:

                    allurls.append(entry['link'])
            except Exception as e :
                    print("getFedd faild")
                    print(e)


        allurls=set(allurls)    
        # print(len(allurls))
        allurls=list(allurls) 
        # print("--------------------------------")
        allNewUrls=[]
        for u in allurls:  
            resp=globalUrlsStore.sadd(domain,u)
            if resp==1:
                allNewUrls.append(u)

                


        if len(allNewUrls)==0:
            allurls="empty"
        # else:
           
            # print("new posts : "+str(len(allNewUrls)))    
            

        return allNewUrls            
                       
    except Exception as e:
        print("len7")

        print(e)       








def downloadFeed(sourcedomain,sourceUrl):
    import readtime
    import time
    import datetime
    ts = time.time()
    time_stamp_dily = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # print(sourcedomain)
    # print(sourceUrl)

    try:

        goFlag=False

        try: 
            article = Article(sourceUrl,keep_article_html=True)
            article.download()
            htmlString=article.html
#             print(htmlString)
            article.parse()
            # article.nlp()
            # article_summary= article.summary
            # article_keywords=article.keywords
            article_summary= ""
            article_keywords=""
            article_html=article.article_html
            article =NewsPlease.from_html(htmlString, url=None)
#             print(article)
            goFlag=True
            

        except Exception as e:
            print("news4k")
            print(e)




        if goFlag:
            date_time_thrushold = "date_less"
            stopByDateFlag=False
            if article.date_publish !=None :
                date_time_thrushold=(article.date_publish).strftime('%Y-%m-%d')
                if date_time_thrushold<"2020-12-11":
                    # print("------------------------------> "+str(date_time_thrushold))
                    stopByDateFlag=True
                # print("-----------------Not stop "+str(date_time_thrushold))    
                date_time_thrushold=(article.date_publish)
            # print("\n")
            # print(date_time_thrushold)    
            result = readtime.of_text(article.maintext)
            readtime=result.seconds
            news={}

            if len(str(article.title))<3000:
                news['title']=str(article.title)
                # news['title_auto_complete']=str(article.title)
            else:
                news['title']=""
                # news['title_auto_complete']=""






            if len(str(article.maintext))<20000:
                news['maintext']=str(article.maintext)
            else:
                news['maintext']=""




            cats = ['movies', 'media', 'news', 'entertainment', 'sports','crime','home','women','war','music','programing','health','politics','furniture','schooling','education','celebrities']
            # print(random.choice(cats))
            news['category']=random.choice(cats)
            # news['date_download']=(article.date_download).strftime('%d/%m/%Y')
            news['date_download']=(str(time_stamp_dily))
            if article.date_publish !=None :
                # news['date_publish']=(article.date_publish).strftime('%d/%m/%Y')
                news['date_publish']=str(article.date_publish)
            else:
                news['date_publish']=str(article.date_publish)


            # news['description']=article.description
            news['image_url']=article.image_url

            news['language']=language_name(str(article.language))

            # news['title_page']=article.title_page
            # news['title_rss']=article.title_rss
            news['source_domain']=sourcedomain
            # news['source_domain_auto_complete']=sourcedomain
            try:
                news['article_length']=len(str(article.maintext))
            except:
                print("len6")

                news['article_length']=None
                
            news['url']=sourceUrl
            news['authors']=article.authors
            # news['article_summary']=article_summary
            news['readtime']=readtime

            # news['article_keywords']=article_keywords

            if len(str(article_html))<20000:
                news['article_html']=str(article_html)
            else:
                news['article_html']=""


            try:
                if news:
                    doc=dumpToElastic(news)
                    return doc
            except Exception as e:

                print("why "+str(e))

    except Exception as e:
        print("newsPlz")
        print(e)
    




def dumpToElastic(article):
    try:

        # data = json.load(f)
        data = article
        go=True

    except json.decoder.JSONDecodeError:
        print("String could not be converted to a JSON")

    if go:
        # data['facebook_shares'] = randrange(10000)
        # data['pinterest_shares'] = randrange(10000)
        # data['reddit_shares'] = randrange(10000)
        # try:
        #     data['region'] = getSiteLoc(str(data['url']))
        # except:
        #     data['region'] = "not found"
        import random


        # data['region'] = "not found"
        data['facebook_shares']=random.randint(0, 999)
        data['twitter_shares']=random.randint(0, 999)
        # data['pinterest']=0
        # data['pinterest']=random.randint(0, 999)

 
        if data['authors'] ==[]:
            data['authors']=["anonymous"]


        if data['date_download'] is not None:
            data['date_download']=data['date_download'].replace(" ", "T")
        else:
            data['date_download']=None

        if data['date_publish'] is not None:
            data['date_publish']=data['date_publish'].replace(" ", "T")
        
        

        if data['date_publish'] == "None":
            data['date_publish']=None



        if "image_url" in article and "title" in article:


            try:
                if len(str(article['image_url']))>4 and len(str(article['title']))>3 and len(str(article['maintext']))>300:    
                    # doc=json.dumps(data)
                    doc=data
                    return doc
            except Exception as e:
                print("getting length crashed "+str(e))

from reachability import Reachability

import time
def basic_func(num):
    try:
        bulkChunk=[]
        globalCounter=0

        while(1):
            try:
                if globalCounter>=100:
                    reachability = Reachability()
                    if reachability.isonline():
                        globalCounter=0

                    else:
                        print("offline")
                        time.sleep(20)

                # print("count: "+str(globalCounter))
                globalCounter=globalCounter+1
                link=todayDB.srandmember("allurls") 
                link=link.decode("utf-8")
                # print(link)

                domain=link
                feed=getFeedUrls(link)
                # pr/int(feed)
                if feed=="empty":
                    reachability = Reachability()
                    if reachability.isonline():
                        todayDB.srem("allurls",link)
                    else:
                        print("offline")
                        time.sleep(10)
                else:
                    for url in feed:
                        try:
                            doc=downloadFeed(domain,url)
                            if  len(doc['title'])>0:
                                # print(doc['title'])
                                doc=json.dumps(doc)
                                bulkChunk.append(doc)

                        
                        except Exception as e:
                            pass
                            # print("len4")
                            # print(e)



                    todayDB.srem("allurls",link)
                # print(str(len(bulkChunk))+"\n --------------------------")

                if len(bulkChunk)>=30:
                    try:
                        print("\nin bulk--------------------------------------------->\n")
                        bulk(es, bulkChunk, index="content_system_v3",request_timeout=400)
                        bulkChunk=[]
                    except Exception as e:
                        bulkChunk=[]
                        print(e)
            except Exception as e:
                if str(e)=="'NoneType' object has no attribute 'decode'":
                    break
                print("while: "+str(e))   




    except Exception as e:
        print("thread broke : "+str(e))
        # print(bulkChunk)       

def multiprocessing_func(x):
    basic_func(x)
    
    
if __name__ == '__main__':
    
    starttime = time.time()
    pool = Pool(processes=30)              # start 4 worker processes
    pool.map(multiprocessing_func, mylist)
    pool.close()
