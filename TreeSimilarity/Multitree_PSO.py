# -*- coding: utf-8 -*-

"""
@File    : Multitree_PSO.py
@Author  : Hangcheng
@Time    : 2021/3/28 13:04
"""

import json


def getCaseInfo(jsonFile):
    """
    json文件读取
    :param jsonFile: 案例的json文件
    :return: 解析过的json文件
    """
    with open(jsonFile, encoding="utf-8") as tree_file:
        return json.load(tree_file)




class Tree:
    def __init__(self,jsonFile):
        self.CaseDate = getCaseInfo(jsonFile)
        self.root =
