# -*- coding: utf-8 -*-
# @Time ： 2021/1/13 11:42
# @Auth ： Cheng
# @File ：MaterialView.py
# @IDE ：PyCharm

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from Materialinfo import *


class Material(QWidget, Ui_MaterialInfo):

	def __init__(self, parent=None):
		super(Material, self).__init__(parent)
		self.setupUi(self)
