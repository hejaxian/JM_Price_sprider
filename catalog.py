#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#加载requests模块，作为爬虫
import requests
#加载数据库模型
from database import db, Price_Catalog, Sprider_log
#加载日期模块
import datetime,pytz

class Catalog(object):
    def __init__(self,cityid):
        self.cityid = cityid

    def update_catalog(self,page=1,pagesize=10):
        #构造请求数据
        form_data = {'params[isLock]':0,'params[cityid]':self.cityid, 'page': page, 'pageSize':pagesize}
        #向服务器获取数据
        url = 'http://www.jmgczj.com/views/getMatPirces.json'
        requests_result = requests.post(url, data=form_data).json()['results']
        # 构建一个空列表
        data = []
        # 处理结果
        for i in requests_result:
            id = int(i['id'])
            try:
                matCount = int(i['matCount'])
            except:
                matCount = 0
            date_str = i['sortDate']
            date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            post_date_str = i['createOn']
            post_date_time = datetime.datetime.strptime(post_date_str, '%Y-%m-%d %H:%M:%S.%f').date()
            pricescope = int(i['pricescope'])
            cityid = int(i['cityid'])
            cata = {'id': id, 'matCount': matCount, 'issueDate': date_time, 'postDate': post_date_time,
                    'pricescope': pricescope, 'cityid': cityid}
            data.append(cata)
        with db.atomic():
            for catalog in data:
                try:
                    Price_Catalog.create(**catalog)
                except:
                    pass
        try:
            catalog_count = len(data)
            log_text = f"更新目录数据{catalog_count}条."
            Sprider_log.create(type="Update_catalog", issue=log_text,
                           time=datetime.datetime.now(pytz.timezone("Asia/Shanghai")))
        except:
            pass
        db.close()

