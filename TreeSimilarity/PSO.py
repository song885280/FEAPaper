# -*- coding: utf-8 -*-

"""
@File    : PSO.py
@Author  : Hangcheng
@Time    : 2021/3/24 16:49
"""

import numpy as np
import matplotlib.pyplot as plt
import treeSim as ts
from HumanJudge import SimCaculater
from Experiment import GetFileList
import math
import os


def GetTestCouples(dir):
    TestCouples = []
    file_list = GetFileList(dir)
    for i in range(0, len(file_list)):
        for j in range(i + 1, len(file_list)):
            case_1 = file_list[i]
            case_2 = file_list[j]
            TestCouples.append([case_1, case_2])
    return TestCouples


def MultiTree(case_1, case_2, PSO, Plist):
    Tree_1 = ts.bulid_tree(case_1)
    Tree_2 = ts.bulid_tree(case_2)

    multi = ts.MultiTree(Tree_1, Tree_2, math.e, Method=0, PSO=PSO, Plist=Plist)
    Data = []
    Similarity = 0
    for item in multi.AllNodes.keys():
        node = ts.MultiNode(multi, item)
        Name = item
        Weight = node.Weight
        Position = node.Position
        if Position == "root":
            Similarity = Weight
    return Similarity


def get_fitness(x, Population):
    """
    获取fitness
    :param Population:
    :param x: 位置
    :return:
    """
    TestCouples = GetTestCouples("src/ALL")
    Sims_MultiTree = []  # 存放所有MultiTree的相似度
    Sims_Human = []
    for i in range(0, Population):
        Sim_MultiTree = MultiTree(TestCouples[i][0],
                                  TestCouples[i][1],
                                  PSO="True",
                                  Plist=x[i])
        Sims_MultiTree.append(pow(100, Sim_MultiTree))
        Sim_Human = SimCaculater(TestCouples[i][0],
                                 TestCouples[i][1])
        Sims_Human.append((pow(100, Sim_Human)))
    return np.abs(np.array(Sims_MultiTree) - np.array(Sims_Human))


class PSO(object):
    def __init__(self, population, max_step, solving_range, learning_rate, bia, dimension):
        """

        :type solving_range: list
        """
        self.max_step = max_step  # 循环的最大部署
        self.dim = dimension  # 搜索的维度
        self.population = population  # 粒子的个数
        self.solving_range = solving_range  # 求解的范围
        self.c1 = self.c2 = learning_rate  # 学习因子，一般为2
        self.w = bia  # 惯性权重

        self.x = np.random.uniform(low=solving_range[0], high=solving_range[1],
                                   size=(self.population, self.dim))

        # 随机初始化粒子的位置

        self.v = np.random.rand(self.population, self.dim)  # 随机初始化粒子的速度

        self.p = self.x  # 目前为止个体好的位置
        fitness = get_fitness(self.x, self.population)  # 计算各点到最优位置的距离

        self.pg = self.x[np.argmin(fitness)]  # 求解全局最小的位置

        self.individual_best_fitness = fitness  # 个体的最优适应度
        self.global_best_fitness = np.min(fitness)  # 全局的最优适应度

    def update(self):
        r1 = np.random.rand(self.population, self.dim)
        r2 = np.random.rand(self.population, self.dim)  # 随机初始化
        self.v = self.w * self.v + self.c1 * r1 * (self.p - self.x) + self.c2 * r2 * (self.pg - self.x)
        self.x = self.v + self.x  # 更新位置和速度
        fitness = get_fitness(self.x, self.population)
        update_id = np.greater(self.individual_best_fitness, fitness)  # 需要更新的个体
        self.p[update_id] = self.x[update_id]
        # 新一代出现了更小的fitness，所以更新全局最优fitness和位置
        if np.min(fitness) < self.global_best_fitness:
            self.pg = self.x[np.argmin(fitness)]
            self.global_best_fitness = np.min(fitness)
        print('最优适应度: %.5f, 平均适应度: %.5f' % (self.global_best_fitness, np.mean(fitness)))

    def evolve(self):
        fig = plt.figure()
        for i in range(self.max_step):
            plt.clf()
            plt.scatter(self.x[:, 0], self.x[:, 1], s=30, color='r')
            plt.xlim(-5, 5)
            plt.ylim(-5, 5)
            plt.pause(0.1)
            self.update()
            plt.show()

        print("本次计算最优解为：", list(self.pg))
        Sim_PSO = MultiTree("src/ALL/大型氧化反应器_模态分析.json",
                            "src/ALL/大型精制反应器_模态分析.json",
                            PSO="True",
                            Plist=self.pg)

        Sim_Multitree = MultiTree("src/ALL/大型氧化反应器_模态分析.json",
                                  "src/ALL/大型精制反应器_模态分析.json",
                                  PSO="False",
                                  Plist=self.pg)

        Sim_Human = SimCaculater("src/ALL/大型氧化反应器_模态分析.json",
                                 "src/ALL/大型精制反应器_模态分析.json")

        print("使用PSO算法：{}，不使用PSO算法：{}，人工标注：{}".format(Sim_PSO, Sim_Multitree, Sim_Human))


if __name__ == '__main__':
    pso = PSO(population=300,
              max_step=100,
              solving_range=[0.80, 1.2],
              learning_rate=2,
              bia=0.6,
              dimension=5)
    pso.evolve()

# if __name__ == '__main__':
#     GetTestCouples("src/ALL")
# [1.0815271979006698, 2.8151620763332366, 1.3357623474818106, 1.4472123480459873, 1.608078508787306]
# max_step=100 high_accuracy
# 
