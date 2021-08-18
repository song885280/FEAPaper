# -*- coding: utf-8 -*-

"""
@File    : plot_w2v.py
@Author  : Hangcheng
@Email   : megamhc@gmail.com
@Time    : 2021/4/7 13:56
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker

plt.rc('font', family='Times New Roman')


def Delta(Sim_1, Sim_2):
    return abs((Sim_1 - Sim_2) / Sim_2)


class Result:

    def __init__(self, filename):
        """

        :param filename: 结果文件名
        """
        self.Data = pd.read_csv(filename, encoding="gbk")
        self.length = self.Data.shape[0] - 1
        self.W2V_Delta = 0
        self.VSM_Delta = 0
        self.W2V_Theta = 0
        self.VSM_Theta = 0
        self.Original_Delta = 0
        self.Original_Theta = 0
        self.BERT_Delta = 0
        self.BERT_Theta = 0

    def AvrDelta(self, Mod):
        """
        计算整体的平均误差
        :param Mod:
        :return: 平均误差
        """
        index = "sim_" + Mod
        AllDelta = 0
        for i in range(0, self.length):
            Sim_1 = self.Data.loc[i][index]
            Sim_2 = self.Data.loc[i]["sim_Human"]
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
            Sim_1 = self.Data.loc[i][index]
            Sim_2 = self.Data.loc[i]["sim_Human"]
            AllTheta += pow(Delta(Sim_1, Sim_2) - avrDelta, 2)
        return AllTheta / self.length


W2V = Result("0425_en_W2V.csv")

W2V.W2V_Delta = W2V.AvrDelta("w2v")
W2V.W2V_Theta = W2V.GetTheta(W2V.W2V_Delta, "w2v")
W2V.VSM_Delta = W2V.AvrDelta("vsm")
W2V.VSM_Theta = W2V.GetTheta(W2V.VSM_Delta, "vsm")
W2V.Original_Delta = W2V.AvrDelta("original")
W2V.Original_Theta = W2V.GetTheta(W2V.Original_Delta, "original")
W2V.BERT_Delta = W2V.AvrDelta("BERT")
W2V.BERT_Theta = W2V.GetTheta(W2V.BERT_Delta, "BERT")

print("W2V:", W2V.W2V_Delta, W2V.W2V_Theta)
print("MultiTree:", W2V.Original_Delta, W2V.Original_Theta)
print("VSM:", W2V.VSM_Delta, W2V.VSM_Theta)
print("BERT:", W2V.BERT_Delta, W2V.BERT_Theta)

fig = plt.gca()
Mods = ["word2vec+multi-tree", "multi-tree", "VSM", "SBERT"]
Delta = [W2V.W2V_Delta, W2V.Original_Delta, W2V.VSM_Delta, W2V.BERT_Delta]
Theta = [W2V.W2V_Theta, W2V.Original_Theta, W2V.VSM_Theta, W2V.BERT_Theta]

plt.bar(Mods, Delta, yerr=Theta, width=0.45, error_kw={'ecolor': '0.2', 'capsize': 5, "capthick": 1}, alpha=0.7)
plt.xticks(fontsize=13)  # 更改字体大小
plt.yticks(fontsize=13)
plt.ylim(0, 0.25)
fig.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))  # 将y轴转换为百分比
plt.ylabel('Average error', fontsize=13)
# plt.title('Error compared with human judgement',fontsize=15)
plt.savefig("img/Error_analysis_w2v_en.svg")
plt.show()
