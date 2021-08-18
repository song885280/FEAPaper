# # -*- coding: utf-8 -*-
#
# """
# @File    : test.py
# @Author  : Hangcheng
# @Email   : megamhc@gmail.com
# @Time    : 2021/4/7 9:18
# """
#
# import numpy as np
# from matplotlib import pyplot as plt
# from scipy.stats import t
#
# # 在5-15范围内生成15个随机数据点
# X = np.random.randint(5, 15, 15)
#
# # 样本大小
# n = X.size
#
# # 平均
# X_mean = np.mean(X)
#
# # standard deviation
# X_std = np.std(X)
#
# # standard error
# X_se = X_std / np.sqrt(n)
# # alternatively:
# #    from scipy import stats
# #    stats.sem(X)
#
# # 95% Confidence Interval
#
# dof = n - 1         # degrees of freedom
# alpha = 1.0 - 0.95
# conf_interval = t.ppf(1-alpha/2., dof) * X_std*np.sqrt(1.+1./n)
#
# fig = plt.gca()
# plt.errorbar(1, X_mean, yerr=X_std, fmt='-o')
# plt.errorbar(2, X_mean, yerr=X_se, fmt='-o')
# plt.errorbar(3, X_mean, yerr=conf_interval, fmt='-o')
#
# plt.xlim([0,4])
# plt.ylim(X_mean-conf_interval-2, X_mean+conf_interval+2)
#
# # axis formatting
# fig.axes.get_xaxis().set_visible(False)
# fig.spines["top"].set_visible(False)
# fig.spines["right"].set_visible(False)
# plt.tick_params(axis="both", which="both", bottom="off", top="off",
#                 labelbottom="on", left="on", right="off", labelleft="on")
#
# plt.legend(['Standard Deviation', 'Standard Error', 'Confidence Interval'],
#            loc='upper left',
#            numpoints=1,
#            fancybox=True)
#
# plt.ylabel('random variable')
# plt.title('15 random values in the range 5-15')
#
# plt.show()

import numpy as np


def cosSim(x, y):
    '''
    余弦相似度
    '''
    tmp = np.sum(x * y)
    non = np.linalg.norm(x) * np.linalg.norm(y)
    return np.round(tmp / float(non), 9)


A = np.load("RelatedFiles/FEA_embedding.npy")
print(cosSim(A[0],A[1]))
