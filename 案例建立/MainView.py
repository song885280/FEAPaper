# -*- coding: utf-8 -*-
# @Time ： 2021/1/11 15:19
# @Auth ： Cheng
# @File ：MainView.py
# @IDE ：PyCharm

import sys
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
		Usage = self.Usage.toPlainText()
		Standard = self.Standard.toPlainText()
		analyseType = self.analyseType.toPlainText()
		designPara = self.designPara.toPlainText()
		Condition = self.Condition.toPlainText()
		Load = self.Load.toPlainText()

		if CaseName == "":
			QMessageBox.information(self, "错误",
			                        "请输入案例名称")
			return
		else:
			QMessageBox.information(self, "成功",
			                        "\"%s\" 案例已成功生成" % CaseName)

		rows = self.MaterialTable.rowCount()

		for rows_index in range(rows):
			# print items[item_index].text()
			[print(self.MaterialTable.item(rows_index, j).text()) for j in range(0, 3)]

	def initTable(self):
		"""
		初始化材料表格
		"""
		for i in range(0, self.MaterialTable.rowCount())[::-1]:  # 删除新增的行
			self.MaterialTable.removeRow(i)

		self.MaterialTable.insertRow(0)

	# print(CaseName, Usage, Standard)
	def addMaterialBtn(self):
		"""
        在材料表格中添加一行
		"""
		row_cnt = self.MaterialTable.rowCount()
		self.MaterialTable.insertRow(row_cnt)


# def resetInterface(self):


if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = MyWindow()
	myWin.show()
	sys.exit(app.exec_())
