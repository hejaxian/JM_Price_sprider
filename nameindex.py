#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#加载数据库模型
from database import JM_Price,XH_Price,EP_Price,KP_Price,TS_Price,Name_Index
#引入多线程
from multiprocessing import Pool

def Get_name(cityid):
    name_list = []
    if cityid == 1:
        p = JM_Price
    elif cityid == 2:
        p = XH_Price
    elif cityid == 3:
        p = EP_Price
    elif cityid == 4:
        p = KP_Price
    elif cityid == 5:
        p = TS_Price

    for i in p.select().iterator():
        if i.name not in name_list:
            name_list.append(i.name)
    return name_list

def Push_to_db(name_list,cityid):
    data = []
    for name in name_list:
        index_data = {'name':name,'cityid':cityid}
        data.append(index_data)
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
