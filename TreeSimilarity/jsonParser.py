# -*- coding: utf-8 -*-
# @Time ： 2020/10/28 12:24
# @Auth ： Cheng
# @File ：jsonParser.py
# @IDE ：PyCharm

import json


def get_relation(data: dict):
    """
	获取案例中所有的is_A关系
	:param data: json文件中的数据
	:return: 包含所有关系的列表
	"""
    relations = []

    def extract(raw_dict):
        keys = list(raw_dict.keys())
        for key in keys:
            child = raw_dict[key]
            for item in child:
                if type(item) == dict:
                    for i in list(item.keys()):
                        relations.append([i, key])
                    extract(item)
                else:
                    relations.append([item, key])

    extract(data)
    # print(relations)
    return relations


def get_nodes(relations):
    """
	从关系中提取信息，获取节点的层级和节点列表
	:return: 返回一个包含各个层级所有节点的列表
	"""
    dict_1 = {}
    for item in relations:
        if item[1] not in list(dict_1.keys()):
            dict_1[item[1]] = []
            dict_1[item[1]].append(item[0])
        else:
            dict_1[item[1]].append(item[0])
    nodes = [[list(dict_1.keys())[0]]]
    for list_1 in nodes:
        this_level = []
        for item in list_1:
            try:
                this_level = this_level + dict_1[item]
            except KeyError:
                pass
            except TypeError:
                print(item)
        if this_level:
            nodes.append(this_level)
    return nodes


def Converter(filename):
    """
	提取文件的信息
	:param filename: 案例文件.json
	"""
    with open(filename, encoding="utf-8") as tree_file:
        raw_data = json.load(tree_file)
        relations = get_relation(raw_data)
        nodes = get_nodes(relations)
        tree_data = {"NODES": nodes, "RELATIONS": relations}
        return tree_data


if __name__ == "__main__":
    # print(Converter("experiment/压力容器.json"))
    # print(Converter("src/ALL/管壳式换热器_热分析.json"))
    print(Converter("src/ALL/半内嵌式带肋外墙板_抗风承载力要求.json"))
