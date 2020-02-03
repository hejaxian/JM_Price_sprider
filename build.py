#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database import *
from catalog import Catalog
from price import Price
from fixdata import Auto_fix_JM
from nameindex import Build_Index
from multiprocessing.dummy import Pool

def build():
    Creat_db()
    print("Created")
    # 生成目录
    city_list = [1, 2, 3, 4, 5]
    for city in city_list:
        Catalog(city).update_catalog(1)
    # 采集价格
    for city in city_list:
        Price(city).update_price(1)
        city_name = ['JM', 'XH', 'EP', 'KP', 'TS']
        index = city - 1 
        print(f'Save {city_name[index]} data.')
    # 修正数据
    Auto_fix_JM()
    # 生成索引
    p = Pool(5)
    for i in city_list:
        p.apply_async(Build_Index, args=(i,))
    p.close()
    p.join()


if __name__ == "__main__":
    #构建数据库
    #try:
    #    Price_Catalog.select().count()
    #except:
    #    build()
    build()