# -*- coding: utf-8 -*-
# @Time ： 2021/2/25 13:40
# @Auth ： Cheng
# @File ：Experiment.py
# @IDE ：PyCharm

import VSM
import math
import os
import pandas
from tqdm import tqdm

import treeSim as ts

All_simPairs = []


def GetFileList(dir):
	file_list = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			file_list.append(os.path.join(root, file))
	return file_list


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
	# 提取近义词对
	Pairs = multi.simPairs
	simPairs_2 = []
	for item in Pairs:
		if item not in simPairs_2:
			if [item[1], item[0]] not in simPairs_2:
				simPairs_2.append(item)

	table = pandas.DataFrame(Data, columns=["None", "Weight", "Position"])
	return table, "{0:.3f}".format(Similarity), simPairs_2


def innerType(TypeName):
	"""
	比较同类案例的平均相似度
	:param TypeName: 类别名
	"""
	All_data = []
	file_list = GetFileList("src/"+TypeName)
	for i in tqdm(range(0, len(file_list))):
		for j in range(i + 1, len(file_list)):
			case_1 = file_list[i]
			case_2 = file_list[j]
			sim_w2v = Comp(file_list[i], file_list[j], "1")[1]
			sim = Comp(file_list[i], file_list[j], "0")[1]
			simPairs = Comp(file_list[i], file_list[j], "1")[2]
			sim_vsm = VSM.VSIm(case_1, case_2)
			All_data.append([case_1, case_2, sim_w2v, simPairs, sim, sim_vsm])
			All_simPairs.extend(simPairs)
	simPairsTable = pandas.DataFrame(All_simPairs, columns=["1", "2"])
	simPairsTable.to_csv("关键词对", encoding="gbk")
	result = pandas.DataFrame(All_data, columns=["案例1", "案例2", "sim_w2v", "simPairs", "sim", "sim_vsm"])
	result.to_csv("results/" + TypeName + "_results.csv", encoding="gbk")


def TypeSide(TypeA, TypeB):
	"""
	比较不同类型的案例之间的相似度
	:param TypeA:
	:param TypeB:
	"""
	All_data = []
	FolderA = TypeA
	FolderB = TypeB
	file_listA = GetFileList("src/usage/" + FolderA)
	file_listB = GetFileList("src/usage/" + FolderB)
	for i in tqdm(range(0, len(file_listA))):
		for j in range(0, len(file_listB)):
			case_1 = file_listA[i]
			case_2 = file_listB[j]
			sim_w2v = Comp(case_1, case_2, "1")[1]
			sim = Comp(case_1, case_2, "0")[1]
			simPairs = Comp(case_1, case_2, "1")[2]
			sim_vsm = VSM.VSIm(case_1, case_2)
			All_data.append([case_1, case_2, sim_w2v, simPairs, sim, sim_vsm])

	result = pandas.DataFrame(All_data, columns=["案例1", "案例2", "sim_w2v", "simPairs", "sim", "sim_vsm"])
	result.to_csv("results/usage/" + FolderA + "_" + FolderB + "_results.csv", encoding="gbk")


def TypeEX():
	"""
	比较类别之间的相似度
	:rtype: object
	"""
	FoldersA = ["传热容器", "储运容器", "分离容器", "反应容器", "容器部件"]
	FoldersB = ["疲劳分析", "应力分析", "热分析", "结构分析"]

	for i in FoldersA:
		for j in FoldersA:
			if i != j:
				TypeSide(i, j)

	# for i in FoldersB:
	# 	for j in FoldersB:
	# 		if i != j:
	# 			TypeSide(i, j)


if __name__ == '__main__':
	# TypeEX()
	innerType("ALL")
	print("Finished")
