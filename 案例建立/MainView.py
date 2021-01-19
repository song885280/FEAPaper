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
		self.Reset.clicked.connect(self.initTable)
		self.Reset.clicked.connect(self.clearText)
		self.addMaterial.clicked.connect(self.addMaterialBtn)
		self.delMaterial.clicked.connect(self.delMaterialBtn)

	def clearText(self):
		"""
		清空文本框
		"""
		self.CaseName.clear()
		self.Usage.clear()
		self.Standard.clear()
		self.analyseType.clear()
		self.ProductPara.clear()
		self.EnviPara.clear()
		self.Condition.clear()
		self.Load.clear()
		self.Position.clear()

	def createBtn(self):
		"""
		建立案例
        """
		CaseName = self.CaseName.toPlainText()

		Usage = self.Usage.toPlainText()

		Standard = self.Standard.toPlainText()

		analyseType = self.analyseType.toPlainText()

		productPara = self.ProductPara.toPlainText()

		enviPara = self.EnviPara.toPlainText()

		Condition = self.Condition.toPlainText()

		Load = self.Load.toPlainText()

		Position = self.Position.toPlainText()

		if CaseName == "" or analyseType == "":
			QMessageBox.information(self, "错误",
			                        "请输入案例名称和分析类型")
			return
		else:

			CaseInfo = {"名称": Separate(CaseName), "关键词": Separate(Usage), "标准": Separate(Standard)}
			WorkingInfo = {"部件": Separate(Position), "工况": Separate(Condition), "载荷": Separate(Load)}
			DesignPara = {"产品参数": Separate(productPara), "环境参数": Separate(enviPara)}

			MaterialInfo = {}
			rows = self.MaterialTable.rowCount()
			for rows_index in range(rows):
				try:
					MaterialName = self.MaterialTable.item(rows_index, 0).text()
					MaterialPara = self.MaterialTable.item(rows_index, 1).text()
					MaterialInfo[MaterialName] = Separate(MaterialPara)
				except AttributeError:
					MaterialName = self.MaterialTable.item(rows_index, 0).text()
					MaterialPara = [""]
					MaterialInfo[MaterialName] = Separate(MaterialPara)

			FEAcase = {"分析案例":
				           [{"产品信息": [CaseInfo],
				             "分析类型": Separate(analyseType),
				             "材料属性": [MaterialInfo],
				             "设计参数": [DesignPara],
				             "计算参数": [WorkingInfo]}]}

			Filename = CaseName + "_" + analyseType
			SaveJson(FEAcase, Filename)
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

	def delMaterialBtn(self):
		"""
		删除一行
		"""
		row_cnt = self.MaterialTable.rowCount()
		self.MaterialTable.removeRow(row_cnt - 1)


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
	with open("JsonFiles/" + fileName + ".json", 'w', encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = MyWindow()
	myWin.showMaximized()
	myWin.show()
	sys.exit(app.exec_())
