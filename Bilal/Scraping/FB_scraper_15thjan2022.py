from asyncio import exceptions
from logging import exception
from facebook_scraper import*
import time
import random
import pymongo
import redis

DB10 = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)
DB11 = redis.Redis(host = '43.251.253.107', port= 1500, db= 11)
myclient = pymongo.MongoClient("mongodb://43.251.253.107:1600/")
mydb = myclient['Facebook-Scraper_15thJan2022']
mycol = mydb['Allposts']

def FBscraper(PAGES,COOKIES):
  # get keys of DB10
  fbPages = []
  keys=DB10.keys()
  for key in keys:
    dkey=key.decode("utf-8")
    fbPages.append(dkey)
  print(len(fbPages))

  pgs = 0
  # fb urls to extract posts data and upload on DB-1
  fields = ('comments','link','likes','images','shared_time','text','post_id','reactions','shares','user_id','time','timestamp','time')
  inPageDelayslist = [10,22,8,12,15,40,7,20,15,30]
  # fbPages = ('ABCNews','cnn','NBCNews','mlive','TheIndependentOnline','thedailybeast','WashingtonExaminer','Gawker','Upworthy','chroncom','Slate','bleacherreport','EliteDaily','washingtonpost','DailyMail','nytimes','BuzzFeed','usatoday','CBSNews','HuffPost')
  for fbp_Key in fbPages:
    try:
      try:

        value = DB10.srandmember(fbp_Key)
        Dvalue = value.decode('utf-8')
        fbp = Dvalue.split('||')[0]
        print(fbp)
      except Exception as e:
        print('decoding error :', e)
        DB11.sadd('D '+fbp_Key,value)
        DB10.delete(fbp_Key)
        break
      time.sleep(random.choice(inPageDelayslist))
      print(fbp)
      psts = 0    
      inPostDelayslist = [10,5,3,12,3,40,7,5]    
      try:
        for post in get_posts(fbp, pages= PAGES ,cookies= COOKIES):
          collection = {'DomainName':fbp_Key, 'pageName':fbp}#add a column of website name  and add a column of FB pagename        
          time.sleep(random.choice(inPostDelayslist))
          for items in fields:
            collection[items] = (post[items])
              
          x = mycol.insert_one(collection)
          psts +=1 #increment posts count
      except Exception as e:
        print('URL Error :', e)
        DB11.sadd('U '+fbp_Key,value)
        DB10.delete(fbp_Key)
        break

      print('number of posts per page: ',psts)
      pgs +=1#increment page count
      DB10.delete(fbp_Key)
      print('number of FB pages scraped: ', pgs)
      if (pgs == 5):
        break
    except exceptions.TemporarilyBanned:
      print("Temporarily banned, sleeping for 10m")
      print('number of FB pages scraped before error : ', pgs)
      time.sleep(3600)
      break

cookiesAdd = ['Cookies_BabarAzam.txt','Cookies_IrfanKhan.txt','Cookies_SaifMagsi.txt']

credentials=random.choice(cookiesAdd)#choose a random cookies file.
count=0 #initialize counter for number of pages scraped to jump to change cookies file and continue scraping.
countacc =0
while(1):
  if(count==2):# if number of pages becomes 'pgs = 20', change cookies file.
    count=0
    credentials=random.choice(cookiesAdd)# choose a random cookies file.
    countacc +=1
    print('number of credentials changed: ', countacc)
  else:  
    print('cookies file used: ',credentials)
    FBscraper(3,credentials)
    count+=1
