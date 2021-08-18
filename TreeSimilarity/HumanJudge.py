# -*- coding: utf-8 -*-

"""
@File    : HumanJudge.py
@Author  : Hangcheng
@Time    : 2021/3/26 20:36
"""

import json
from VSM import booleanW, cosDis

def getCaseInfo(jsonFile):
    """
    json文件读取
    :param jsonFile: 案例的json文件
    :return: 解析过的json文件
    """
    with open(jsonFile, encoding="utf-8") as tree_file:
        return json.load(tree_file)


def clearList(listA):
    listB = []
    for item in listA:
        if item not in listB:
            listB.append(item)
        else:
            continue
    return listB


def compare(listA, listB):
    """
    :param listA: 列表1
    :param listB: 列表2
    :return: 列表1和2的VSM相似度
    """
    nodes = list(set(listA + listB))
    vectorA = booleanW(listA, nodes)
    vectorB = booleanW(listB, nodes)
    Similarity = cosDis(vectorA, vectorB)
    return Similarity


def SimCaculater(FileA, FileB):
    CaseA = BuildCase(FileA)
    CaseB = BuildCase(FileB)
    ProductSim = 0.3 * compare(CaseA.ProductInfo, CaseB.ProductInfo)  # 产品
    AnalyseSim = 0.4 * compare(CaseA.AnalyseType, CaseB.AnalyseType)  # 分析类型
    PropertyTypeSim = 0.05 * compare(CaseA.PropertyType, CaseB.PropertyType)  # 材料牌号
    PropertyInfoSim = 0.05 * compare(CaseA.ProductInfo, CaseB.ProductInfo)  # 材料属性
    DesignSim = 0.2 * compare(CaseA.DesignPara, CaseB.DesignPara)  # 设计参数

    Similarity = 0.55 * (ProductSim + AnalyseSim + PropertyTypeSim + PropertyInfoSim + DesignSim ) + 0.45
    # print("产品相似度：{0:.2f}".format(ProductSim))
    # print("分析相似度：{0:.2f}".format(AnalyseSim))
    # print("材料相似度：{0:.2f}".format(PropertyTypeSim + PropertyInfoSim))
    # print("设计相似度：{0:.2f}".format(DesignSim))
    # print("计算相似度：{0:.2f}".format(CaculateSim))
    # print("案例相似度：{0:.2f}".format(Similarity))
    return Similarity

class BuildCase:
    '''
    计算中文案例
    '''
    def __init__(self, jsonFile):
        Case = getCaseInfo(jsonFile)["分析案例"][0]
        self.ProductInfo = Case["产品信息"][0]["设备名称"] + \
                           Case["产品信息"][0]["部件名称"] + \
                           Case["产品信息"][0]["设计要求"]

        self.AnalyseType = Case["目的信息"]

        self.PropertyType = list(Case["材料信息"][0].keys())

        self.PropertyInfo = []
        for i in self.PropertyType:
            self.PropertyInfo += Case["材料信息"][0][i]
        self.PropertyInfo = clearList(self.PropertyInfo)

        self.DesignPara = Case["工况"][0]["设计工况"] + Case["工况"][0]["工作工况"]
#
# class BuildCase:
#     '''
#     计算英文案例
#     '''
#     def __init__(self, jsonFile):
#         Case = getCaseInfo(jsonFile)["FEA task"][0]
#         self.ProductInfo = Case["Product information"][0]["Equipment name"] + \
#                            Case["Product information"][0]["Part name"] + \
#                            Case["Product information"][0]["Design requirement"]
#
#         self.AnalyseType = Case["Analysis aim"]
#         self.PropertyType = list(Case["Material and physical data"][0].keys())
#         self.PropertyInfo = []
#         for i in self.PropertyType:
#             self.PropertyInfo += Case["Material and physical data"][0][i]
#         self.PropertyInfo = clearList(self.PropertyInfo)
#
#         self.DesignPara = Case["Working condition"][0]["Design condition"] + Case["Working condition"][0]["Operation " \
#                                                                                                           "condition"]



# 测试代码
# a = BuildCase("src/ALL/LNG低温卧式储罐_强度分析.json")
# b = BuildCase("src/ALL/LNG储罐主容器_热分析.json")
## SimCaculater("src/ALL/LNG低温卧式储罐_强度分析.json","src/ALL/LNG储罐主容器_热分析.json")
