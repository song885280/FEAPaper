# -*- coding: utf-8 -*-
# @Time ： 2021/1/11 15:19
# @Auth ： Cheng
# @File ：MainView.py
# @IDE ：PyCharm

import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from mainWindow import *
from MaterialView import Material


class MyWindow(QMainWindow, Ui_MainWindow):

	def __init__(self, parent=None):
		super(MyWindow, self).__init__(parent)
		self.setupUi(self)
		self.Create.clicked.connect(self.createBtn)
		self.Create.clicked.connect(self.initTable)
		self.addMaterial.clicked.connect(self.addMaterialBtn)

	def createBtn(self):
		"""
        :param self:
        :return:
        """
		CaseName = self.CaseName.toPlainText()
		self.CaseName.clear()

		Usage = self.Usage.toPlainText()
		self.Usage.clear()

		Standard = self.Standard.toPlainText()
		self.Standard.clear()

		analyseType = self.analyseType.toPlainText()
		self.analyseType.clear()

		designPara = self.designPara.toPlainText()
		self.designPara.clear()

		Condition = self.Condition.toPlainText()
		self.Condition.clear()

		Load = self.Load.toPlainText()
		self.Load.clear()

		if CaseName == "":
			QMessageBox.information(self, "错误",
			                        "请输入案例名称")
			return
		else:

			CaseInfo = {"名称": Separate(CaseName), "用途": Separate(Usage), "标准": Separate(Standard)}
			WorkingInfo = {"工况": Separate(Condition), "载荷": Separate(Load)}

			MaterialInfo = {}
			rows = self.MaterialTable.rowCount()
			for rows_index in range(rows):
				Position = self.MaterialTable.item(rows_index, 0).text()
				MaterialName = self.MaterialTable.item(rows_index, 1).text()
				MaterialPara = self.MaterialTable.item(rows_index, 2).text()
				MaterialInfo[Position] = {MaterialName: Separate(MaterialPara)}

			FEAcase = {"分析案例":
				           [{"产品信息": [CaseInfo],
				             "分析类型": [Separate(analyseType)],
				             "材料属性": [MaterialInfo],
				             "设计参数": Separate(designPara),
				             "计算参数": [WorkingInfo]}]}
			print(FEAcase)
			SaveJson(FEAcase, CaseName)
			QMessageBox.information(self, "成功",
			                        "\"%s\" 案例已成功生成" % CaseName)

	def initTable(self):
		"""
		初始化材料表格
		"""
		for i in range(0, self.MaterialTable.rowCount())[::-1]:  # 删除新增的行
			self.MaterialTable.removeRow(i)

		self.MaterialTable.insertRow(0)

	def addMaterialBtn(self):
		"""
        在材料表格中添加一行
		"""
		row_cnt = self.MaterialTable.rowCount()
		self.MaterialTable.insertRow(row_cnt)


def Separate(Text):
	"""
	分隔输入的文本
	:param Text: String
	"""
	if "，" in Text:
		return Text.split("，")
	else:
		return [Text]


def SaveJson(data, fileName):
	with open("JsonFiles/" + fileName + ".json", 'w',encoding="utf-8") as f:
		json.dump(data, f,ensure_ascii=False)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = MyWindow()
	myWin.show()
	sys.exit(app.exec_())
