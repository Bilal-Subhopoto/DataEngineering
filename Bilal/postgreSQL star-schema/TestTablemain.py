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
    ForeignKey
)
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker


# BASE_DIR=os.path.dirname(os.path.realpath(__file__))
DATABASE_URI = 'postgresql://postgres:pta123456@127.0.0.1:5432/Synthetic_FB'
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


class TestTable(Base):
    __tablename__='Staging_Synthetic_FB'
    id=Column(Integer(),primary_key=True)
    
    domain_name=Column(TEXT(),nullable=False)
    page_name=Column(TEXT(),nullable=False)
    user_id=Column(TEXT(),nullable=False)
    date_download=Column(DATE(),nullable=False)
    post_text =Column(TEXT())#this should be unique and on conflict do nothing, in that case foreign key will have to be searched for by table entry, not immediately after insert into
    post_id=Column(TEXT(),nullable=False)
    link=Column(TEXT())
    post_likes=Column(Integer())
    post_shares=Column(Integer())

    def __repr__(self):
        return f"<Domain {self.domain_name}>"


Base.metadata.create_all(engine) #creates the database
session=sessionmaker()(bind=engine)
