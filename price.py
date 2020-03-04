#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#加载requests模块，作为爬虫
import requests
#加载数据库模型
from database import db,Price_Catalog,JM_Price,XH_Price,EP_Price,KP_Price,TS_Price,Sprider_log
#加载日期模块
import datetime,pytz
#引入多线程
from multiprocessing.dummy import Pool

class Price(object):
    def __init__(self,cityid):
        city_list = [1,2,3,4,5]
        database_list = [JM_Price,XH_Price,EP_Price,KP_Price,TS_Price]
        cityid_index = city_list.index(cityid)
        self.database = database_list[cityid_index]
        self.cityid = cityid

    def get_price(self,journalId):
        #构造请求数据
        form_data = {'params[specclass]':'','params[keyword]':'','params[journalId]':journalId,'params[spec]':'','page':'1','pageSize':1000000}
        headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Accept':'application/json, text/javascript, */*; q=0.01'}
        #向服务器获取数据
        url = 'http://www.jmgczj.com/views/getPriceList.json'
        requests_result = requests.post(url, data=form_data,headers=headers).json()['results']
        # 构建一个空列表
        data = []
        # 处理结果
        for i in requests_result:
            id = int(i['id'])
            # 过滤掉两个分割线
            if id == 0 or id == 999999999999:
                pass
            else:
                # 材料分类
                specclass, subclass = i['specclass'], i['subclass']
                # 材料名称、规格、单位、品牌
                name, spec, unit, brand = i['name'], i['spec'], i['unit'], i['brand']
                # 价格
                price = float(i['price'])
                # 除税价
                if i['notaxPrice'] is not None:
                    notaxPrice = float(i['notaxPrice'])
                else:
                    notaxPrice = 0.0

                if i['taxRate'] is not None:
                    taxRate = float(i['taxRate'])
                else:
                    taxRate = 0.0
                # 城市、备注、journalID
                cityid, note, journalId = int(i['cityid']), i['note'], int(i['journalId'])
                price_data = {'id': id, 'specclass': specclass, 'subclass': subclass, 'name': name, 'spec': spec,
                              'unit': unit,'brand': brand, 'price': price, 'notaxPrice': notaxPrice,
                              'taxRate': taxRate,'cityid': cityid, 'journalId': journalId, 'note': note
                              }
                data.append(price_data)
        #插入数据库
        self.database.insert_many(data).execute()
        # 到更改目录中exist_price的数值
        query = Price_Catalog.update(exist_price=True).where(Price_Catalog.id == journalId)
        query.execute()
        # 修复日期
        date_query = Price_Catalog.get(Price_Catalog.id==journalId)
        RQ = self.database.update(issueDate=date_query.issueDate).where(self.database.journalId == journalId)
        RQ.execute()

    def update_price(self,mode=0):
        new_journalId_list = []
        Query = Price_Catalog.select().where(
            (Price_Catalog.cityid == self.cityid) & (Price_Catalog.exist_price == False) & (Price_Catalog.pricescope == 0)
        )
        db.close()
        for i in Query:
            new_journalId_list.append(i.id)
        p = Pool(5)
        for i in new_journalId_list:
            p.apply_async(self.get_price, args=(i,))
            query = Price_Catalog.update(exist_price=True).where(Price_Catalog.id == i)
            query.execute()
        p.close()
        p.join()
        if mode ==0 and len(new_journalId_list) > 0:
            updated_journalId = ','.join('%s' % id for id in new_journalId_list)
            log_text = f"本次更新记录{len(new_journalId_list)}条"
            
            Sprider_log.create(type="Update_price", issue=log_text,
            	time=datetime.datetime.now(pytz.timezone("Asia/Shanghai")))
            	
            db.close()
