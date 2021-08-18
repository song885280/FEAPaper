'''
提取一列，算分布
'''
import json

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
'''
file_path = r'G:\0425_W2V.csv'
data_frame_csv = pd.read_csv(file_path, names = ["sim_Human"], header=2, usecols = [3])
data_df01 = data_frame_csv[['sim_Human']]
print(type(data_df01))

data_df01 = data_frame_csv['sim_Human']
print(type(data_df01))
res = data_df01.tolist()
print(res)
print('列表长度为：'+ str(res.__len__() + 1))

# 绘图
np.random.seed(0)
plt.figure(dpi=120)
sns.set(style='dark')
sns.set_style("dark", {"axes.facecolor": "#e9f3ea"})#修改背景色
chart1 = sns.distplot(res, hist=True, kde=False, color="#098154")
# chart2 = sns.kdeplot(res, shade=True, bw=0.5, color="#098154")
plt.title('sim_w2v',fontsize=15)
plt.show()

#  提取FEA案例中的中英文案例
data = pd.read_excel('FEA案例数据_中英文扩充.xlsx')
data_v = data.values
pd.DataFrame([[data_v[j, i] for i in range(0, len(data.columns), 1)]
        for j in range(0, len(data_v), 2)], columns = list(data.columns)[::1]).\
    to_excel('FEA案例数据_中文400.xlsx', index = False)
'''

#
# -*- coding:utf-8 -*-

file_in = open("2.json", "r", encoding='utf8')
json_data = json.load(file_in)
print(type(json_data))
for key, value in json_data.items():
    print('key:'+ str(key))
    print('value:'+ str(value))

print('---test---')

file_out = open("2.1.json", "w")
file_out.write(json.dumps(json_data))

file_in.close()
file_out.close()


'''
def process_json(input_json_file, output_json_file):
    file_in = open(input_json_file, "r", encoding='utf8')
    file_out = open(output_json_file, "w",encoding='utf8')
    # load数据到变量json_data
    json_data = json.load(file_in)
    print
    json_data
    print
    "after update  --->"
    print
    type(json_data)
    # 修改json中的数据
    json_data["[]"] = "[none]"
    print
    json_data

    # 将修改后的数据写回文件
    file_out.write(json.dumps(json_data))
    file_in.close()
    file_out.close()


process_json("2.json", "2.1.json")
print()

'''



