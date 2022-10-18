#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#加载数据库模型
from database import *
import re
import datetime
#引入多线程
from multiprocessing import Pool

Query = JM_Price.select()
#清除所有项目特征中的Null
def Cleannull():
    spec = ''
    Q =  JM_Price.update(spec=spec).where(JM_Price.spec.is_null(True))
    Q.execute()

#修复混凝土名称、规格
def PT_hnt():
    hunningtu_type = ['商品普通混凝土','泵送普通混凝土']
    biaohao_list = ['C10','C15','C20','C25','C30','C35','C40','C45','C50']
    for type in hunningtu_type:
        type_name = type
        for biaohao in biaohao_list:
            name = biaohao + type_name
            spec = biaohao
            Q = JM_Price.update(name=type_name,spec=spec).where(JM_Price.name==name)
            Q.execute()

def BS_hnt():
    biaohao_list = ['C10', 'C15', 'C20', 'C25', 'C30', 'C35', 'C40', 'C45', 'C50']
    for biaohao in biaohao_list:
        bengsong_biaodashi = biaohao+'.*泵送'
        bengsong = JM_Price.select().where( (JM_Price.name=='普通混凝土')&(JM_Price.spec.regexp(bengsong_biaodashi)) )
        a = JM_Price.update(name='泵送普通混凝土',spec=biaohao).where( (JM_Price.name=='普通混凝土')&(JM_Price.spec.regexp(bengsong_biaodashi)) )
        a.execute()
        b = JM_Price.select().where( (JM_Price.name=='普通混凝土')&(JM_Price.spec.contains(biaohao)&(~(JM_Price.spec << bengsong))))
        for i in b:
            i.name ='商品普通混凝土'
            i.spec = biaohao
            i.save()

def FS_hnt():
    hunningtu_type = ['商品S6-S8防水混凝土', '泵送商品S6-S8防水混凝土']
    biaohao_list = ['C10','C15','C20','C25','C30','C35','C40','C45','C50']
    for type in hunningtu_type:
        type_name = type
        for biaohao in biaohao_list:
            name = biaohao+type_name
            spec = biaohao+' S6-S8'
            Q = JM_Price.update(name=type_name,spec=spec).where(JM_Price.name==name)
            Q.execute()


 #高档材料
def GD_cailiao():
    gaodang_list = ['热镀锌钢塑(衬塑)复合管','热镀锌钢管',
                    '球墨铸铁管','球墨法兰短管','球墨推插弯头45°','球墨推插弯头90°','球墨双承弯头90°','球墨大小头',
                    '球墨梳杰','球墨推插法兰三叉',
                    'PP-R直通','PVC-U45°异径斜三通',
                    '室内消防栓']
    for i in gaodang_list:
        new_name = i+'(高档)'
        Q = JM_Price.update(name=new_name,note='').where( (JM_Price.note == '高档材料综合价格')&(JM_Price.name==i))
        Q.execute()

#修复钢筋
def GJ_YG():
    Q1 = JM_Price.update(spec='HPB235 Φ10mm以內').where(JM_Price.spec=='HPB235 Φ10以內')
    Q2 = JM_Price.update(spec='HPB300 Φ10mm以內').where(JM_Price.spec=='HPB300 Φ10以內')
    Q3 = JM_Price.update(spec='HPB235 Φ12-14mm').where(JM_Price.spec=='HPB235 Φ12-14')
    Q4 = JM_Price.update(spec='HPB300 Φ12-14mm').where(JM_Price.spec=='HPB300 Φ12-14')
    Q5 = JM_Price.update(spec='HPB235 Φ16-25mm').where(JM_Price.spec=='HPB235 Φ16-25')
    Q6 = JM_Price.update(spec='HPB300 Φ16-25mm').where(JM_Price.spec=='HPB300 Φ16-25')
    Q7 = JM_Price.update(spec='HPB235 Φ25mm以外').where(JM_Price.spec=='HPB235 Φ25以外')
    Q8 = JM_Price.update(spec='HPB300 Φ25mm以外').where(JM_Price.spec=='HPB300 Φ25以外')
    Q1.execute()
    Q2.execute()
    Q3.execute()
    Q4.execute()
    Q5.execute()
    Q6.execute()
    Q7.execute()
    Q8.execute()

def GJ_LWG():
    Q1 = JM_Price.update(spec='HRB335 Φ10mm以內').where(
        ((JM_Price.spec.contains('10以內'))|(JM_Price.spec.contains('10mm以內')))&(JM_Price.spec.contains('HRB335'))
    )
    Q2 = JM_Price.update(spec='HRB335 Φ12-14mm').where(
        (JM_Price.spec.contains('12-14')) & (JM_Price.spec.contains('HRB335'))
    )
    Q3 = JM_Price.update(spec='HRB335 Φ16-25mm').where(
        (JM_Price.spec.contains('16-25')) & (JM_Price.spec.contains('HRB335'))
    )
    Q4 = JM_Price.update(spec='HRB335 Φ25mm以外').where(
        ((JM_Price.spec.contains('25以外'))|(JM_Price.spec.contains('25mm以外'))) & (JM_Price.spec.contains('HRB335'))
    )
    Q5 = JM_Price.update(spec='HRB400 Φ10mm以內').where(
        ((JM_Price.spec.contains('10以內'))|(JM_Price.spec.contains('10mm以內'))) & (JM_Price.spec.contains('HRB400'))
        & (~(JM_Price.spec.contains('HRB400E')))
    )
    Q6 = JM_Price.update(spec='HRB400 Φ12-14mm').where(
        (JM_Price.spec.contains('12-14')) & (JM_Price.spec.contains('HRB400')) & (~(JM_Price.spec.contains('HRB400E')))
    )
    Q7 = JM_Price.update(spec='HRB400 Φ16-25mm').where(
        (JM_Price.spec.contains('16-25')) & (JM_Price.spec.contains('HRB400')) & (~(JM_Price.spec.contains('HRB400E')))
    )
    Q8 = JM_Price.update(spec='HRB400 Φ25mm以外').where(
        ((JM_Price.spec.contains('25以外'))|(JM_Price.spec.contains('25mm以外'))) & (JM_Price.spec.contains('HRB400'))
        & (~(JM_Price.spec.contains('HRB400E')))
    )
    Q9 = JM_Price.update(spec='HRB400E Φ10mm以內').where(
        ((JM_Price.spec.contains('10以內'))|(JM_Price.spec.contains('10mm以內'))) & (JM_Price.spec.contains('HRB400E'))
    )
    Q10 = JM_Price.update(spec='HRB400E Φ12-14mm').where(
        (JM_Price.spec.contains('12-14')) & (JM_Price.spec.contains('HRB400E'))
    )
    Q11 = JM_Price.update(spec='HRB400E Φ16-25mm').where(
        (JM_Price.spec.contains('16-25')) & (JM_Price.spec.contains('HRB400E'))
    )
    Q12 = JM_Price.update(spec='HRB400E Φ25mm以外').where(
        ((JM_Price.spec.contains('25以外'))|(JM_Price.spec.contains('25mm以外'))) & (JM_Price.spec.contains('HRB400E'))
    )
    Q1.execute()
    Q2.execute()
    Q3.execute()
    Q4.execute()
    Q5.execute()
    Q6.execute()
    Q7.execute()
    Q8.execute()
    Q9.execute()
    Q10.execute()
    Q11.execute()
    Q12.execute()

def RQ(cityid):
    list = Price_Catalog.select().where(Price_Catalog.cityid==cityid)
    database_list = [JM_Price, XH_Price, EP_Price, KP_Price, TS_Price]
    list_index_num = cityid -1
    Query = database_list[list_index_num]
    for i in list:
        Q = Query.update(issueDate=i.issueDate).where((Query.journalId==i.id)&(Query.issueDate.is_null(True)))
        Q.execute()

def Autofull_Date():
    cityid_list = [1,2,3,4,5]
    TP = Pool(2)
    TP.map(RQ, cityid_list)
    TP.close()
    TP.join()

#自动修复
def Auto_fix_JM():
    function_list = [Cleannull, PT_hnt, BS_hnt, FS_hnt, GD_cailiao, GJ_YG, GJ_LWG, RQ]
    pool = Pool(2)
    for func in function_list:
        pool.apply_async(func)
    pool.close()
    pool.join()

if __name__ == "__main__" :
    Auto_fix_JM()
