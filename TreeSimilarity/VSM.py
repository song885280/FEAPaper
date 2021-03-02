# -*- coding: utf-8 -*-
# @Time ： 2020/11/9 13:33
# @Auth ： Cheng
# @File ：VSM.py
# @IDE ：PyCharm

import jsonParser
import numpy as np


def mergeList(Tree):
	"""
	合并案例树的每一层的节点
	:param Tree: 案例树
	"""
	T = jsonParser.Converter(Tree)
	merged = []
	for item in T["NODES"]:
		merged = merged + item
	return merged


def iniVectorSpace(tree1: str, tree2: str):
	"""
	构建向量空间
	:param tree1: 案例树1
	:param tree2: 案例树2
	"""
	T1 = mergeList(tree1)
	T2 = mergeList(tree2)
	nodes = list(set(T1 + T2))
	return T1, T2, nodes


def booleanW(T, Nodes):
	"""
	使用布尔权重
	:param T: 案例中的节点
	:param Nodes: 所有节点
	"""
	L = []
	# 特征词出现则权重为1，不出现则为0
	for item in Nodes:
		if item in T:
			L.append(1)
		else:
			L.append(0)
	vector = np.array(L)
	return vector


def cosDis(V1, V2):
	"""
	计算向量的余弦相似度
	:param V1: 树1的特征向量
	:param V2: 树2的特征向量
	"""
	d = np.linalg.norm(V1) * np.linalg.norm(V2)
	return np.dot(V1, V2) / d


def VSIm(case_1,case_2):
	Tree1 = case_1
	Tree2 = case_2
	L1, L2, allNode = iniVectorSpace(Tree1, Tree2)
	vector_1 = booleanW(L1, allNode)
	vector_2 = booleanW(L2, allNode)
	S = cosDis(vector_1, vector_2)
	return  S
