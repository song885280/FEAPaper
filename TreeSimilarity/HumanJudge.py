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
    PropertyTypeSim = 0.05 * compare(CaseA.PropertyType, CaseB.PropertyType)  # 材料类型
    PropertyInfoSim = 0.05 * compare(CaseA.ProductInfo, CaseB.ProductInfo)  # 材料信息
    DesignSim = 0.1 * compare(CaseA.DesignPara, CaseB.DesignPara)  # 设计参数
    CaculateSim = 0.1 * compare(CaseA.CaculatePara, CaseB.CaculatePara)  # 计算参数

    Similarity = 0.5 * (ProductSim + AnalyseSim + PropertyTypeSim + PropertyInfoSim + DesignSim + CaculateSim) + 0.5
    # print("产品相似度：{0:.2f}".format(ProductSim))
    # print("分析相似度：{0:.2f}".format(AnalyseSim))
    # print("材料相似度：{0:.2f}".format(PropertyTypeSim + PropertyInfoSim))
    # print("设计相似度：{0:.2f}".format(DesignSim))
    # print("计算相似度：{0:.2f}".format(CaculateSim))
    # print("案例相似度：{0:.2f}".format(Similarity))
    return "{0:.1f}".format(Similarity)


class BuildCase:
    def __init__(self, jsonFile):
        Case = getCaseInfo(jsonFile)["分析案例"][0]

        self.ProductInfo = Case["产品信息"][0]["名称"] + \
                           Case["产品信息"][0]["关键词"] + \
                           Case["产品信息"][0]["标准"]

        self.AnalyseType = Case["分析类型"]

        self.PropertyType = list(Case["材料属性"][0].keys())

        self.PropertyInfo = []
        for i in self.PropertyType:
            self.PropertyInfo += Case["材料属性"][0][i]
        self.PropertyInfo = clearList(self.PropertyInfo)

        self.DesignPara = Case["设计参数"][0]["产品参数"] + Case["设计参数"][0]["环境参数"]

        self.CaculatePara = Case["计算参数"][0]["部件"] + \
                            Case["计算参数"][0]["工况"] + \
                            Case["计算参数"][0]["载荷"]

# a = BuildCase("src/ALL/LNG低温卧式储罐_强度分析.json")
# b = BuildCase("src/ALL/LNG储罐主容器_热分析.json")
#
# SimCaculater("src/ALL/LNG低温卧式储罐_强度分析.json","src/ALL/LNG储罐主容器_热分析.json")
