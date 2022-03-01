#user
#posts
from datetime import datetime
from enum import unique
from http.client import CONFLICT
import os
from sqlite3 import Date
from typing import Text
from sqlalchemy import (
    create_engine,
    Integer,
    Column,
    String,
    ForeignKey,
    text
)
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker


# BASE_DIR=os.path.dirname(os.path.realpath(__file__))
DATABASE_URI = 'postgresql://postgres:pta123456@127.0.0.1:5432/sqlalchemy'
# conn='sqlite:///'+os.path.join(BASE_DIR,'blog.db')


engine=create_engine(DATABASE_URI)


Base=declarative_base()


"""
class User:
    id:int pk
    username:str
    email:str


class Post:
    id:int pk
    title:str
    content:str
    user_id:int foreignkey
"""


class Domain(Base):
    __tablename__='domain'
    id=Column(Integer(),primary_key=True)
    domain_name=Column(String(100),nullable=False)
    engagementd=relationship('Engagement',back_populates='domain_key',cascade='all, delete')

    def __repr__(self):
        return f"<Domain {self.domain_name}>"

class Page(Base):
    __tablename__='page'
    id=Column(Integer(),primary_key=True)
    page_name=Column(String(100),nullable=False)#this should be unique and on conflict do nothing, in that case foreign key will have to be searched for by table entry, not immediately after insert into
    
    engagementp=relationship('Engagement',back_populates='page_key',cascade='all, delete')

    def __repr__(self):
        return f"<Page {self.page_name}>"


class User(Base):
    __tablename__='user'
    id=Column(Integer(),primary_key=True)
    user_id=Column(String(50),nullable=False)#this should be unique and on conflict do nothing, in that case foreign key will have to be searched for by table entry, not immediately after insert into
    
    engagementu=relationship('Engagement',back_populates='user_key',cascade='all, delete')

    def __repr__(self):
        return f"<User {self.user_id}>"

class Post_Time(Base):
    __tablename__='post_time'
    id=Column(Integer(),primary_key=True)
    time_download=Column(String(220),nullable=False)#this should be unique and on conflict do nothing, in that case foreign key will have to be searched for by table entry, not immediately after insert into
    
    engagementt=relationship('Engagement',back_populates='post_time_key',cascade='all, delete')

    def __repr__(self):
        return f"<Post_Time {self.time_download}>"

class Content(Base):
    __tablename__='content'
    id=Column(Integer(),primary_key=True)
    post_text =Column(TEXT())#this should be unique and on conflict do nothing, in that case foreign key will have to be searched for by table entry, not immediately after insert into
    post_id=Column(String(255),nullable=False)
    link=Column(TEXT())
    engagementc=relationship('Engagement',back_populates='content_key',cascade='all, delete')

    def __repr__(self):
        return f"<Content {self.post_id}>"



class Engagement(Base):
    __tablename__='engagement'
    id=Column(Integer(),primary_key=True)
    post_likes=Column(Integer(),nullable=False)
    post_shares=Column(Integer(),nullable=False)
    post_comments=Column(Integer(),nullable=False)
   
    domain_id=Column(Integer(),ForeignKey('domain.id'))
    page_id = Column(Integer(),ForeignKey('page.id'))
    userID=Column(Integer(),ForeignKey('user.id'))
    post_timeID = Column(Integer(),ForeignKey('post_time.id'))
    content_id=Column(Integer(),ForeignKey('content.id'))
    

    domain_key=relationship('Domain',back_populates='engagementd')
    page_key=relationship('Page',back_populates='engagementp')
    user_key=relationship('User',back_populates='engagementu')
    post_time_key=relationship('Post_Time',back_populates='engagementt')
    content_key=relationship('Content',back_populates='engagementc')
    


    
    def __repr__(self):
        return f"<Domain {self.post_likes}>"


Base.metadata.create_all(engine) #creates the database
session=sessionmaker()(bind=engine)
