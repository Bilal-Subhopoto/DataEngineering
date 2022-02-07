import time
from tkinter import E
from pymongo import MongoClient
from datetime import date, datetime

myclient = MongoClient("mongodb://43.251.253.107:1600/")#?keepAlive=true&poolSize=30&autoReconnect=true&socketTimeoutMS=360000&connectTimeoutMS=360000")
# MONGO_URI=mongodb://user:password@127.0.0.1:27017/dbname?keepAlive=true&poolSize=30&autoReconnect=true&socketTimeoutMS=360000&connectTimeoutMS=360000
#source collection 
sdb = myclient['Copy_FB_scraper_MT2']
scol = sdb['Allposts']
#target database
tdb = myclient['test']


def insertDoc(field,value,col,document):
    tcol = tdb[col]#target collection
    d_doc = {}
    
    d_doc[field] = document[value]
    # print(d_doc)
    if tcol.count_documents(d_doc) != 0:
        id = tcol.find_one(d_doc)
        
        # print(field," Already Exist")
        
        return id["_id"]
    else:
        
        if field == "timeDownload":
            # datetime_object = datetime.strptime(document[value])
            datetime_object = datetime.fromisoformat(str(document[value]))
            time_doc = {}                               
            time_doc[field] = datetime_object
            print("Inserting new...", field)
            id = tcol.insert_one(time_doc)    
            # print("_id: ", type(id.inserted_id))
            return id.inserted_id
            # ISODate("2022-01-26T17:46:00.679Z")

        else:
            print("Inserting new...", field)
            id = tcol.insert_one(d_doc)
            # print("_id: ", type(id.inserted_id))
            return id.inserted_id
def insertCon(col,document):
    
    tcol = tdb[col]#target collection  
    c_doc = {}
    c_doc["text"] = document["text"]
    c_doc["link"] = document["link"]   
    c_doc["postID"] = document["post_id"]   
    
    if tcol.count_documents(c_doc) != 0:
        id = tcol.find_one(c_doc)        
        # print("Content Already Exist")
        return id["_id"]
    else:
        print("Inserting new content")
        # print(c_doc)
        id = tcol.insert_one(c_doc)
        
        return id.inserted_id

    
    

i = 0
docList = []
# timeOut = datetime.now()
cursor = scol.find({},{ "_id": 0},no_cursor_timeout=True)
for doc in cursor:#later we can query using timeDownload field to return only the documents with specific date.
    try:
        dom_id  = insertDoc("domain","DomainName","Domain",doc)
        pg_id = insertDoc("page","pageName","Page",doc)
        us_id = insertDoc("userID","user_id","User",doc)
        td_id = insertDoc("timeDownload","TimeDownload","Time_dim",doc)
        con_id = insertCon("Content",doc)
        
        mycol = tdb["Engagement"]#target collection  
        e_doc = {}
        e_doc["likes"] = doc["likes"]
        e_doc["shares"] = doc["shares"]       
        e_doc["comments"] = doc["comments"]
        e_doc["Domain"] = dom_id
        e_doc["Page"] = pg_id
        e_doc["User"] = us_id
        e_doc["Time_dim"] = td_id
        e_doc["Content"] = con_id

        
        if mycol.count_documents(e_doc) != 0:
            # mycol.find_one(e_doc)        
            # print("Already Exist")
            pass
            
        else:
            print("Appending New Doc")
            docList.append(e_doc) 
            # print(e_doc)
            # tt = datetime.now()
            # if (tt.hour != timeOut.hour):
            #     timeOut = datetime.now()
            # if (abs(tt.minute-timeOut.minute) in range (10,13)) & (len(docList)>0):#insert docList documents every 10-12 minutes & not optimal yet
            if len(docList)==50:
                i+=len(docList)#using this timeout condition 9635 docs are bulk inserted at first iteration, 7309,6887,6275,6267(36373)
                print("Bulk Inserting ",len(docList)," new Docs")
                mycol.insert_many(docList)
                docList = []
                # timeOut = datetime.now()
                

            print(i," New Documents Inserted in Fact")
    except Exception as e:
        print(e)
        cursor.close()  # <- Don't forget to close the cursor
cursor.close()  # <- Don't forget to close the cursor
    
