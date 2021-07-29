# # -*- coding: utf-8 -*-
# # @Time ： 2020/11/3 14:31
# # @Auth ： Cheng
# # @File ：伪代码.py
# # @IDE ：PyCharm
#
# for each node: # 对MFT中的每一个节点
# 	# 比较其与相同层级的各节点的相似度，取最大值
# 	Delta = max{Compare node with other nodes of the same level}
# 	if 0.6 < Delta < 1:  # 如果该最大值大于0.6且小于1
# 		node.Delta = Delta  # 则将其作为该节点的Delta值
# 	else:
# 		node.Delta = 0 # 则该节点的Delta值为0
#
# 	if node.position == "leaf": # 如果节点为叶节点
# 		if node in Tree1 and Tree2:
# 			node.Weight = 0
# 		else:
# 			node.Weight = node.Delta
#
# 	if node.position = "branch":
# 		if node in T1 and node in T2:
# 			γ = 0
# 		else:
# 			γ = node.Delta
# 		θ = sum(node.Children.Weight) / β # β 子节点的个数
# 		Weight = (1 - 1 / (α ** L(node))) * θ \
# 		         + (1 / (α ** L(node))) * γ #  α 阻尼系数，取e（2.71）
#
# 	if node.position = "root":
# 		Weight = sum(node.Children.Weight) / β
# 		Similarity = Weight
# return Similarity