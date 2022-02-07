from pymongo import MongoClient

myclient = MongoClient("mongodb://43.251.253.107:1600/")
mydb = myclient['Copy_FB_scraper_MT2']
mycol = mydb['Allposts']

def CopyFromColl1ToColl2(database1,collection1,database2,collection2):
    db1 = MongoClient('mongodb://43.251.253.107:1600/')[database1][collection1]
    db2 = MongoClient('mongodb://43.251.253.107:1600/')[database2][collection2]
    #here you can put the filters you like.
    for a in db1.find():
        try:
            db2.insert(a)
            print(a)
        except:
            print('did not copy')

# You can choose the database name and the collection name
CopyFromColl1ToColl2('FB_scraper_MT2','Allposts','Copy_FB_scraper_MT2','Allposts')