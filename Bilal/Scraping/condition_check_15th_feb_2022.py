import redis
from urlextract import URLExtract
import datetime
from bson.objectid import ObjectId
import tldextract

MasterDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 7)#masterDB

StateDB = redis.Redis(host = '43.251.253.107', port= 1500, db= 10)#stateDB
DB11 = redis.Redis(host = '43.251.253.107', port= 1500, db= 11)#for error links
globalPostIDstate = redis.Redis(host = '43.251.253.107', port= 1500, db= 8)#all the seen postIDs

from log21 import get_logger, get_colors

logger = get_logger("LOG21", show_time=False)


def searchURLinText(postText,FB_key):    
    extractor = URLExtract()
    urls = extractor.find_urls(postText)
    # urls = str(urls)
    for url in urls:     
        url = tldextract.extract(url)
        link = tldextract.extract(FB_key)
        print("searchURLinText "+url.domain+"  -  "+link.domain)

        if url.domain == link.domain:
            return True
            break
    return False
def searchURL(postLink,FB_key):
    URL = tldextract.extract(postLink)
    links = tldextract.extract(FB_key)
    print("searchURL "+URL.domain +"  -  "+links.domain)

    if URL.domain == links.domain:
        return True
    else:
        return False

posts =[ 
# /* 1 */
{
    "_id" : ObjectId("61f14288e416ac412f18440b"),
    "DomainName" : "jagoinvestor.com",
    "pageName" : "Jagoinvestor.blog",
    "comments" : 0,
    "link" : "jagoinvestor.com/blog",
    "likes" : 0,
    "images" : [ 
        "https://scontent-sjc3-1.xx.fbcdn.net/v/t39.30808-6/fr/cp0/e15/q65/269768188_4726902077398583_7255539214094077338_n.jpg?_nc_cat=100&ccb=1-5&_nc_sid=110474&_nc_ohc=uv2NyDCkJkUAX9RpuMK&_nc_ht=scontent-sjc3-1.xx&oh=00_AT95BBp4JBVKSzEbxec4s-CJlWRyohGcV_O2mcdluYBneg&oe=61F53874"
    ],
    "shared_time" : None,
    "text" : "Starting audio webinar in 1 hr (at 5:30 pm)\n\nTopic : Bonds vs debt fund\n\nLink to Telegram group : https://t.me/+CFH852EKThw0OWZl",
    "post_id" : "4726902150731909",
    "reactions" : None,
    "shares" : 0,
    "user_id" : "765661936855970",
    "time" : datetime.datetime(2022,1,8),#("2022-01-08T16:08:48.000Z"),
    "timestamp" : 1641640128,
    "TimeDownload" : datetime.datetime(2022,1,26)#ISODate("2022-01-26T17:46:00.679Z")
},

# /* 2 */
{
    "_id" : ObjectId("61f14289290f7277b818440b"),
    "DomainName" : "theforwardcabin.com",
    "pageName" : "theforwardcabin",
    "comments" : 0,
    "link" : None,
    "likes" : 0,
    "images" : [],
    "shared_time" : None,
    "text" : "What are your travel plans for this month? Going anywhere exciting? Comment below for a chance to win a $5 Amazon Gift Card!  theforwardcabin.com/abc",
    "post_id" : "4721091164633785",
    "reactions" : None,
    "shares" : 0,
    "user_id" : "570766772999599",
    "time" : datetime.datetime(2022,1,1),#ISODate("2022-01-01T22:00:36.000Z"),
    "timestamp" : 1641056436,
    "TimeDownload" : datetime.datetime(2022,1,26)#ISODate("2022-01-26T17:46:01.030Z")
},

# /* 3 */
{
    "_id" : ObjectId("61f1428b442d19040b18440b"),
    "DomainName" : "mszgnews.com",
    "pageName" : "mszgnews",
    "comments" : 0,
    "link" : "mszgnews.com",
    "likes" : 0,
    "images" : [ 
        "https://scontent.fcgk17-1.fna.fbcdn.net/v/t39.30808-6/fr/cp0/e15/q65/270106959_462945768790046_5539515453997218015_n.jpg?_nc_cat=106&ccb=1-5&_nc_sid=8024bb&_nc_ohc=W8dwM5i6vGYAX9gYE_y&_nc_ht=scontent.fcgk17-1.fna&oh=00_AT_BfAjHDwlEWa-Rmd-IemCoDFoB5OBOYfsncSYENxqDlw&oe=61F59630"
    ],
    "shared_time" : None,
    "text" : "Today marks the day that Guru Gobind Singh Ji of #Gurmat_Ji passed away. He was a Sikh religious figure who sacrificed his life to preserve peace within society, and he will always be remembered as one such martyr!\n#GuruGobindSingh #Sikh #Guru",
    "post_id" : "462945805456709",
    "reactions" : None,
    "shares" : 0,
    "user_id" : "102222478195712",
    "time" : datetime.datetime(2022,1,1),#ISODate("2022-01-10T05:56:47.000Z"),
    "timestamp" : 1641776207,
    "TimeDownload" : datetime.datetime(2022,1,26)#ISODate("2022-01-26T17:46:03.755Z")
},

# /* 4 */
{
    "_id" : ObjectId("61f1428c290f7277b818440c"),
    "DomainName" : "theforwardcabin.com",
    "pageName" : "theforwardcabin",
    "comments" : 1,
    "link" : None,
    "likes" : 0,
    "images" : [],
    "shared_time" : None,
    "text" : "What are your travel plans for this month? Going anywhere exciting? Comment below for a chance to win a $5 Amazon Gift Card! pakistan.com   theforwardcabin.com",
    "post_id" : "4604092409666995",
    "reactions" : None,
    "shares" : 0,
    "user_id" : "570766772999599",
    "time" : datetime.datetime(2021,12,1),#ISODate("2021-12-01T22:01:28.000Z"),
    "timestamp" : 1638378088,
    "TimeDownload" : datetime.datetime(2022,1,26)#ISODate("2022-01-26T17:46:04.515Z")
},

# /* 5 */
{
    "_id" : ObjectId("61f1428de416ac412f18440c"),
    "DomainName" : "jagoinvestor.com",
    "pageName" : "Jagoinvestor.blog",
    "comments" : 0,
    "link" : None,
    "likes" : 10,
    "images" : [ 
        "https://scontent-sjc3-1.xx.fbcdn.net/v/t39.30808-6/fr/cp0/e15/q65/260811976_4569032516518874_7373073743543685203_n.jpg?_nc_cat=111&ccb=1-5&_nc_sid=da1649&_nc_ohc=gbGizoMAsYMAX9WMnZ3&_nc_ht=scontent-sjc3-1.xx&oh=00_AT_zO1Ss07MrINErUjFWEJj9AOJ-EucaDISPfEkJOfTGjg&oe=61F6C289"
    ],
    "shared_time" : None,
    "text" : "Does money increases happiness?\n\nYES.. and here is how its done!!!\n\nKudos to Kartik 🙏",
    "post_id" : "4569032529852206",
    "reactions" : None,
    "shares" : 0,
    "user_id" : "765661936855970",
    "time" : datetime.datetime(2021,11,25),#ISODate("2021-11-25T08:25:02.000Z"),
    "timestamp" : 1637810702,
    "TimeDownload" : datetime.datetime(2022,1,26)#ISODate("2022-01-26T17:46:05.903Z")
}
]
countglobalStateinserted = 0


for post in posts:
    # try:


    # for post in i:
    # print("############################Post",post)
    globalStateinserted = globalPostIDstate.sadd(post["pageName"],post["post_id"])#fbp = post["pageName"] here
    urlfoundinText=False
    urlfoundinText = searchURLinText(post["text"],post["DomainName"])#fbp_key = post["DomainName"]
    urlfound=False
    
    if post["link"] is not None:
        urlfound = searchURL(post["link"],post["DomainName"])#fbp_key = post["DomainName"]
    else:
        print("post['link]  is empty")   

    print("urlfoundinText: "+str(urlfoundinText))
    print("urlfound: "+str(urlfound))

    if urlfoundinText or urlfound:
        logger.info(get_colors('000128000', 'BackWhite') + 'Link Found in post!' )

        print(post["link"])
        print(post["text"])
        print("+++++++++++++++++++++++++++++++++++++++++")
#00efeb

        if globalStateinserted == 0:#in case the post exists in global... 
            countglobalStateinserted +=1
            logger.info(get_colors('#ef4c00', 'BackWhite') + 'Link already exists in state redis '+str(countglobalStateinserted) )

            



        from datetime import datetime
        # if post["time"] is not None:post["time"] is never null/for loop through all the MT2 database and check if "time" is empty in any doc.
        if post["time"].date()<datetime.now().date():#(check if (post post["time"].date is less than datetime.now().date) or (countglobalStateinserted == 3):
            print(post["time"].date())
            print(datetime.now().date())
            logger.info(get_colors('#ef0044', 'BackWhite') + 'Breaking loop after seeing old post'+str(countglobalStateinserted) )

            
            
        if countglobalStateinserted == 3:
            logger.info(get_colors('#ef0044', 'BackWhite') + 'Breaking loop after 3 times link found in state'+str(countglobalStateinserted) )
        # except Exception as e:
        #     print(e)       
    else:
        logger.info(get_colors('red', 'BackWhite') + 'Link not found in post :')
        print(post["link"])
        print(post["text"])
        print("------------------------------------------------------")
    logger.info(get_colors('#008888') + 'next!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')   

