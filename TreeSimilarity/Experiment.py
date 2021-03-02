# -*- coding: utf-8 -*-
# @Time ： 2021/2/25 13:40
# @Auth ： Cheng
# @File ：Experiment.py
# @IDE ：PyCharm

import treeSim as ts
import pandas
import math
import VSM
import os
import sys


def GetFileList(Dir):
	files = []
	for root, dirs, files in os.walk(Dir):
		for file in files:
			files.append(os.path.join(root, file))
	return files


def Comp(case_1, case_2, mod):
	"""
	比较两个案例之间的相似度
	:param mod: 比较方式
	:param case_1: 案例1的名称
	:param case_2: 案例2的名称
	"""
	Tree_1 = ts.bulid_tree(case_1)
	Tree_2 = ts.bulid_tree(case_2)

	multi = ts.MultiTree(Tree_1, Tree_2, math.e, mod)
	Data = []
	Similarity = 0
	for item in multi.AllNodes.keys():
		node = ts.MultiNode(multi, item)
		Name = item
		Weight = node.Weight
		Position = node.Position
		if Position == "root":
			Similarity = Weight
		Data.append([Name, Weight, Position])
	table = pandas.DataFrame(Data, columns=["None", "Weight", "Position"])
	return table, "{0:.3f}".format(Similarity)


if __name__ == '__main__':
	All_data = []
	file_list = GetFileList("json")
	for i in range(0, len(file_list)):
		for j in range(i, len(file_list)):
			case_1 = file_list[i]
			case_2 = file_list[j]
			sim_w2v = Comp(file_list[i], file_list[j], "1")[1]
			sim = Comp(file_list[i], file_list[j], "0")[1]
			sim_vsm = VSM.VSIm(case_1, case_2)
			All_data.append([case_1, case_2, sim_w2v, sim, sim_vsm])
	result = pandas.DataFrame(All_data, columns=["案例1", "案例2", "sim_w2v", "sim", "sim_vsm"])
	result.to_csv("结果.csv", encoding="gbk")
