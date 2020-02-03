#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database import *
from catalog import Catalog
from price import Price
from fixdata import Auto_fix_JM,Autofull_Date
from nameindex import Build_Index
from multiprocessing.dummy import Pool

if __name__ == "__main__":
    #更新目录
    city_list = [1,2,3,4,5]
    for city in city_list:
        Catalog(city).update_catalog(0)
    #采集价格
    for city in  city_list:
        Price(city).update_price(0)
    #修正数据
    Autofull_Date()
    Auto_fix_JM()
    #生成索引
    p = Pool(5)
    for i in city_list:
        p.apply_async(Build_Index, args=(i,))
    p.close()
    p.join()