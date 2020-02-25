from sqlalchemy import Column, Integer, String, Text #, DateTime
from QBlog.database import Base
from datetime import datetime
#from flask import jsonify
import json

class TimeJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def Querytojson(Query):
    jsonData_list = [] #list
    for value in Query:
        res = {} #dict
        res['Id'] = value[0]
        res['Title'] = value[1]
        res['Up_time'] = value[2].strftime('%Y-%m-%d %H:%M:%S')
        jsonData_list.append(res)
    return jsonData_list

class Article(Base):
    __tablename__ = 't_article'
    Id = Column(Integer, primary_key = True, autoincrement = True)
    Author = Column(String(10))
    Title = Column(String(50))
    Abstract = Column(String(255))
    Content = Column(Text)
    Up_time = Column(String(50))#DateTime

    def __init__(self, Author=None, Title=None, Abstract=None, Content=None, Up_time=None):
        self.Author = Author
        self.Title = Title
        self.Abstract = Abstract
        self.Content = Content
        self.Up_time = Up_time

    def __repr__(self):
        #return '<User %s>' % self.username
        return json.dumps({'Author':self.Author, 'Title':self.Title, 'Abstract':self.Abstract, 'Content':self.Content, 'Up_time':self.Up_time},cls=TimeJson)#时间JSON化
