#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from peewee import *
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase('MYSQL_DATABASE',host='MYSQL_HOST',port=MYSQL_PORT,passwd='MYSQL_PASSWD',user='MYSQL_USER',charset='utf8mb4', max_connections=128,stale_timeout=300)
class BaseModel(Model):
    class Meta:
        database = db

class Price_Catalog(BaseModel):
    id, matCount = PrimaryKeyField(), IntegerField()
    issueDate, postDate = DateField(), DateField()
    pricescope, cityid  = IntegerField(), IntegerField()
    exist_price = BooleanField(default=False)

class Sprider_log(BaseModel):
    type, issue = CharField(), CharField()
    time = DateTimeField()

class BasePrice(BaseModel):
    id = IntegerField()
    #材料分类
    specclass, subclass = CharField(null=True), CharField(null=True)
    #名称、规格、单位、品牌
    name, spec, unit, brand = CharField(), CharField(null=True), CharField(null=True), CharField(null=True)
    #含税价、除税价、税率
    price = FloatField()
    #除税价格
    notaxPrice, taxRate, note = FloatField(), FloatField(), CharField(null=True)
    #城市、信息价时间、journalID
    cityid, issueDate, journalId = IntegerField(), DateField(null=True), IntegerField()

class JM_Price(BasePrice):
    pass
class XH_Price(BasePrice):
    pass
class EP_Price(BasePrice):
    pass
class KP_Price(BasePrice):
    pass
class TS_Price(BasePrice):
    pass

class Name_Index(BaseModel):
    id = AutoField()
    name = CharField()
    cityid = IntegerField()

def Creat_db():
	db.create_tables([ 
        Sprider_log, Price_Catalog, Name_Index,
        JM_Price, XH_Price, EP_Price, KP_Price, TS_Price
    ])
