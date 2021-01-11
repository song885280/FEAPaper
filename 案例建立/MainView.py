# -*- coding: utf-8 -*-
# @Time ： 2021/1/11 15:19
# @Auth ： Cheng
# @File ：MainView.py
# @IDE ：PyCharm

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWindow import *


class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.Create.clicked.connect(self.button)

    def button(self):
        """
        :param self:
        :return:
        """
        print(self.Usage.toPlainText())
        print(self.Case_name.toPlainText())


if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = MyWindow()
	myWin.show()
	sys.exit(app.exec_())
