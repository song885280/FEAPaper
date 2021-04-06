# -*- coding: utf-8 -*-

"""
@File    : plot.py
@Author  : Hangcheng
@Email   : megamhc@gmail.com
@Time    : 2021/4/6 20:57
"""

import pandas as pd


def Delta(Sim_1, Sim_2):
    return abs((Sim_1 - Sim_2) / Sim_2)


class Result:

    def __init__(self, filename):
        """

        :param filename: 结果文件名
        """
        self.Data = pd.read_csv(filename, encoding="gbk")
        self.length = self.Data.shape[0] - 1
        self.PSO_Delta = 0
        self.VSM_Delta = 0
        self.PSO_Theta = 0
        self.VSM_Theta = 0

    def AvrDelta(self, Mod):
        """
        计算整体的平均误差
        :param Mod:
        :return: 平均误差
        """
        index = "sim_" + Mod
        AllDelta = 0
        for i in range(0, self.length):
            Sim_1 = self.Data.loc[test.length][index]
            Sim_2 = self.Data.loc[test.length]["sim_Human"]
            AllDelta += Delta(Sim_1, Sim_2)
        return AllDelta / self.length

    def GetTheta(self, avrDelta, Mod):
        """
        计算方差
        :param avrDelta: 平均误差
        :param Mod: 算法名PSO、VSM、Original
        :return: 方差
        """
        index = "sim_" + Mod
        AllTheta = 0
        for i in range(0, self.length):
            Sim_1 = self.Data.loc[test.length][index]
            Sim_2 = self.Data.loc[test.length]["sim_Human"]
            AllTheta += pow(Delta(Sim_1, Sim_2) - avrDelta, 2)
        return AllTheta / self.length


test = Result("ALL_PSO.csv")

test.PSO_Delta = test.AvrDelta("PSO")
test.PSO_Theta = test.GetTheta(test.PSO_Delta, "PSO")

print(test.PSO_Delta, test.PSO_Theta)
