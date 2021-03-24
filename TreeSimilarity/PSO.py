# -*- coding: utf-8 -*-

"""
@File    : PSO.py
@Author  : Hangcheng
@Time    : 2021/3/24 16:49
"""

import numpy as np
import matplotlib.pyplot as plt


def get_fitness(x):
    return np.sum(np.square(x), axis=1)


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

        fitness = get_fitness(self.x)  # 计算各点到最优位置的距离

        self.pg = self.x[np.argmin(fitness)]  # 求解全局最小的位置

        self.individual_best_fitness = fitness  # 个体的最优适应度
        self.global_best_fitness = np.min(fitness)  # 全局的最优适应度

    def update(self):
        r1 = np.random.rand(self.population, self.dim)
        r2 = np.random.rand(self.population, self.dim)  # 随机初始化
        self.v = self.w * self.v + self.c1 * r1 * (self.p - self.x) + self.c2 * r2 * (self.pg - self.x)
        self.x = self.v + self.x  # 更新位置和速度
        fitness = get_fitness(self.x)
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
            plt.xlim(self.solving_range[0], self.solving_range[1])
            plt.ylim(self.solving_range[0], self.solving_range[1])
            plt.pause(0.01)
            self.update()
            plt.show()


pso = PSO(population=50,
          max_step=20,
          solving_range=[-10, 10],
          learning_rate=2,
          bia=0.6,
          dimension=2)
pso.evolve()
