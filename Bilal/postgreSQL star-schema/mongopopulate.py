from telnetlib import theNULL
from pymongo import MongoClient
from main import Engagement,Domain,Page,User,Post_Time,Content,session
import time
from datetime import datetime
from log21 import get_logger, get_colors

logger = get_logger("LOG21", show_time=False)


start = datetime.now()
start1 = start.strftime("%m/%d/%Y, %H:%M:%S")
logger.info(get_colors('#ef4c00', 'BackWhite') + start1)

def CopyFromColl1ToColl2(database1,collection1):
    nonenull = 0
    null = 0
    db1 = MongoClient('mongodb://43.251.253.107:1600/')[database1][collection1]
    
    #here you can put the filters you like.
    
    for a in db1.find():
        
        
        try:
            logger.info(get_colors('#ef4c00', 'BackWhite') +str(nonenull)+" Documents inserted")
            logger.info(get_colors('#ef4c00', 'BackWhite') +str(null)+" Erroneous documents")
            
            
            if (a['DomainName']!=None) & (a['pageName']!=None) & (a['user_id']!=None) & (a['post_id']!=None) & (a["TimeDownload"]!=None):
                print(a['DomainName'])
                print(a['pageName'])
                print(a['user_id'])
                print(a['post_id'])
                print(a['likes'])
                print(a['shares'])
                print(a['comments'])
                print(a["TimeDownload"])
                nonenull+=1
                
                domain = session.query(Domain).filter(Domain.domain_name==a['DomainName']).first()
                print("domain: ", domain)
                if domain:
                    print("domain id already exists: ", domain.id)
                    new_domain = domain
                else:
                    new_domain=Domain(
                        domain_name=a['DomainName']
                    )
                    session.add(new_domain)

                page = session.query(Page).filter(Page.page_name==a['pageName']).first()
                if page:
                    print("page id already exists: ", page.id)
                    new_page = page
                else:
                    new_page = Page(
                        page_name = a["pageName"]
                    )
                    session.add(new_page)
                
                user = session.query(User).filter(User.user_id==a['user_id']).first()
                if user:
                    print("user id already exists: ", user.id)
                    new_user = user
                else:
                    new_user = User(
                        user_id = a["user_id"]
                    )
                    session.add(new_user)

                curDT = a["TimeDownload"]
                curdts = curDT.strftime("%m/%d/%Y, %H:%M:%S")

                post_time = session.query(Post_Time).filter(Post_Time.time_download==curdts).first()
                if post_time:
                    print("post_time id already exists: ", post_time.id)
                    new_post_time = post_time
                else:
                    # curDT = a["TimeDownload"]
                    new_post_time = Post_Time(
                        time_download = curdts
                    )
                    session.add(new_post_time)
                
                content = session.query(Content).filter((Content.post_text==a['text']),(Content.post_id==a['post_id']),(Content.link==a['link'])).first()
                if content:
                    print("content id already exists: ", content.id)
                    new_content = content
                else:
                    # logger.info(get_colors('#ef4c00', 'BackWhite') + str(len(a["text"][0:190]))+" "+str(len(a["text"])))


                    new_content = Content(
                        post_text =  a["text"],
                        post_id =  a["post_id"],
                        link = a["link"]
                    )
                    session.add(new_content)
                
                
                session.commit()

                session.flush()
                # At this point, the object f has been pushed to the DB, 
                # and has been automatically assigned a unique primary key id

                # print(new_domain.id,new_page.id,new_user.id,new_post_time.id,new_content.id)
                # is None

                session.refresh(new_domain)
                session.refresh(new_page)
                session.refresh(new_user)
                session.refresh(new_post_time)
                session.refresh(new_content)

                # refresh updates given object in the session with its state in the DB
                # (and can also only refresh certain attributes - search for documentation)

                print(new_domain.id,new_page.id,new_user.id,new_post_time.id,new_content.id)
                print("#########################################")
                print(new_domain,new_page,new_user,new_post_time,new_content)
                # is the automatically assigned primary key ID given in the database.


                # ddomain=session.query(Domain).filter(Domain.id==new_domain.id).first()
                # print("ddomain: ", ddomain.id)
                # if domain/user/pagename is null or "":
                #     print()
                new_eng=Engagement(
                    post_likes = a["likes"],
                    post_shares = a["shares"],
                    post_comments = a["comments"],
                    domain_key=new_domain,
                    page_key = new_page,
                    user_key = new_user,
                    post_time_key = new_post_time,
                    content_key = new_content
                )

                session.add(new_eng)
                session.commit()

                # print(f"Post cREATED {post['title']}")


                # f = Foo(bar=x)
                # session.add(f)
                session.flush()
                # At this point, the object f has been pushed to the DB, 
                # and has been automatically assigned a unique primary key id

                print(new_eng.id)
                # is None

                session.refresh(new_eng)
                # refresh updates given object in the session with its state in the DB
                # (and can also only refresh certain attributes - search for documentation)

                print(new_eng.id)
                
                # is the automatically assigned primary key ID given in the database.


                # engagement=session.query(Engagement).filter(Engagement.id==1).first()
            else:
                null+=1
                logger.info(get_colors('#ef4c00', 'BackWhite') +str(nonenull)+" Documents inserted")
                logger.info(get_colors('#ef4c00', 'BackWhite') +str(null)+" Erroneous documents")    
                logger.info(get_colors('#ef4c00', 'BackWhite') +"else body start")
                print(a['DomainName'])
                print(a['pageName'])
                print(a['user_id'])
                print(a['post_id'])
                print(a["TimeDownload"])
                logger.info(get_colors('#ef4c00', 'BackWhite') +"else body end")
                time.sleep(8)
        except Exception as e:
            logger.info(get_colors('#ef4c00', 'BackWhite') +str(nonenull)+" Documents inserted")
            logger.info(get_colors('#ef4c00', 'BackWhite') +str(null)+" Erroneous documents")
            print(e)
            break
    

# You can choose the database name and the collection name
CopyFromColl1ToColl2('Copy_FB_scraper_MT2','Allposts')
print("\n")
end = datetime.now()
end1 = end.strftime("%m/%d/%Y, %H:%M:%S")
time = end - start
logger.info(get_colors('#ef4c00', 'BackWhite') +end1)
logger.info(get_colors('#ef4c00', 'BackWhite') +"total time taken: "+str(time))






