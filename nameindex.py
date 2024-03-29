#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#加载数据库模型
from database import db,JM_Price,XH_Price,EP_Price,KP_Price,TS_Price,Name_Index
#引入多线程
from multiprocessing import Pool

def Get_name(cityid):
    name_list = []
    city_list = [1, 2, 3, 4, 5]
    database_list = [JM_Price, XH_Price, EP_Price, KP_Price, TS_Price]
    cityid_index = city_list.index(cityid)
    database = database_list[cityid_index]
    for i in database.select():
        if i.name not in name_list:
            name_list.append(i.name)
    return name_list

def Push_to_db(name_list,cityid):
    data = []
    for name in name_list:
        index_data = {'name':name, 'cityid':cityid}
        data.append(index_data)
    #print(data)
    Name_Index.insert_many(data).execute()

def Build_Index(cityid):
    name_list = Get_name(cityid)
    Push_to_db(name_list,cityid)

if __name__ == "__main__":
    p = Pool(5)
    city_pool = [1, 2, 3, 4, 5]
    for i in city_pool:
        p.apply_async(Build_Index, args=(i,))
    p.close()
    p.join()
