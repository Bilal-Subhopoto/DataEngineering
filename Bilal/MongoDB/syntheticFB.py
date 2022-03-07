from distutils.ccompiler import new_compiler
from pydoc import text
import random
from re import S
from turtle import shearfactor
from xml import dom
import redis
from random import randint,choice
from lorem_text import lorem
from datetime import datetime
import pymongo
from log21 import get_logger, get_colors
from datetime import datetime, timedelta ,date

start = datetime.now()
print(start)
logger = get_logger("LOG21", show_time=False)

base = datetime(2021,1,1)
numdays = 30
date_list = [base + timedelta(days=x) for x in range(numdays)]
inc  = [0,1,3,5,0,6,0,10]


#database connectiones
DB7 = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB
myclient = pymongo.MongoClient("mongodb://43.251.253.107:1600/")
mydb = myclient['Synthetic_FB_Data']
mycol = mydb['9000posts']
newcol = mydb['Allposts']
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def generatePosts():
    for domain in DB7.keys():
        domain = domain.decode('utf-8')#from redis
        pageName = (DB7.srandmember(domain)).decode('utf-8')#from redis
        for i in range(10):

            link = domain+"/"+str(random_with_N_digits(10))
            text = lorem.sentence()
            likes = 0
            shares = 0
            post_id = str(random_with_N_digits(7))
            user_id = str(random_with_N_digits(5))
            dateDownload = datetime(2021,1,1)
            mydoc = {
                    'domain': domain,
                    'pageName' : pageName,
                    'link' : link,
                    'text' : text,
                    'likes' : likes,
                    'shares' : shares,
                    'post_id' : post_id,
                    'user_id' : user_id,
                    'dateDownload' : dateDownload 
                    }
            mycol.insert_one(mydoc)

    logger.info(get_colors('#ef4c00', 'BackWhite') + str(mycol.count_documents({})))

generatePosts()
then = datetime.now() 
print(then - start)

def incPosts():
    posts = mycol.find()
    for post in posts:
               
        try:
            for j in date_list:                
                
                post['likes'] += random.choice(inc)                
                post['shares'] += random.choice(inc)
                post['dateDownload'] = j

                del post['_id']
              
                newcol.insert_one(post)
                           
        except Exception as e:
            print("exception:::::",e)
            break
    
incPosts()
logger.info(get_colors('#ef4c00', 'BackWhite') + str(newcol.count_documents({})))
print(datetime.now()-then)



    