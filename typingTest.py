from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import functools
import environment
import agent
import sys
import pygame as pg
# %matplotlib inline


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(692, 477)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
		font = QtGui.QFont()
		font.setPointSize(14)
		self.textEdit.setFont(font)
		self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.textEdit.setObjectName("textEdit")
		self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
		self.splitter = QtWidgets.QSplitter(self.centralwidget)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		self.splitter.setObjectName("splitter")
		self.widget = QtWidgets.QWidget(self.splitter)
		self.widget.setObjectName("widget")
		self.gridLayout = QtWidgets.QGridLayout(self.widget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.pushButton = QtWidgets.QPushButton(self.widget)
		self.pushButton.setObjectName("pushButton")
		self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
		self.pushButton_2 = QtWidgets.QPushButton(self.widget)
		self.pushButton_2.setObjectName("pushButton_2")
		self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
		self.label = QtWidgets.QLabel(self.widget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.widget)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
		self.gridLayout_2.addWidget(self.splitter, 1, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		self.pushButton.clicked.connect(self.startTest)
		self.pushButton_2.clicked.connect(self.resetTest)
		self.textEdit.textChanged.connect(self.textEdit_callback)
		self.textEdit.setDisabled(True)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		#Added code here
		self.work = WorkThread() #Work Thread
		self.startTime=None
		self.inputNum=0 #All keyboard inputNum
		self.inputNumLast = 0
		self.wpm=None #Word per minute
		self.ipm=None #Input per minute

	def startTest(self):
		self.textEdit.setPlaceholderText("")
		self.textEdit.setDisabled(False)
		self.work.start()
		self.startTime=time.time()
		self.environment = environment.GridWorld()
		self.agentQ = agent.Q_Agent(self.environment)
		self.update_call= functools.partial(self.updateInfo, environment=self.environment, agent = self.agentQ)
		pg.mixer.init()
		self.work.trigger.connect(self.update_call)

	def resetTest(self):
		self.work.quit()
		self.inputNum=0
		self.textEdit.setPlainText("")
		self.textEdit.setDisabled(True)
		self.label.setText("WPM:-")
		self.label_2.setText("IPM:-")

	def updateInfo(self, environment, agent):
		#Calculate time interval
		time_interval=None
		time_interval=(time.time()-self.startTime)/60

		#Just keep characters from textEdit
		text=self.textEdit.toPlainText()
		temp=filter(str.isalpha, text)
		new_text=''.join(list(temp))
		print(new_text)

		if self.inputNumLast == 0:
			wpm=round((len(new_text)/5)/5)
			ipm= self.inputNum/5
			self.inputNumLast = self.inputNum
		else:
			print('!!')
			wpm=round((len(new_text)/5)/5)
			ipm=(self.inputNum - self.inputNumLast)/5
			self.inputNumLast = self.inputNum

		# print(time_interval)
		# print(self.inputNum)
		# print(len(new_text))
		# print("----------")
		self.label.setText("WPM:"+str(wpm))
		self.label_2.setText("IPM:"+str(ipm))	

		old_state = self.environment.current_location
		action = agent.choose_action(self.environment.actions)
		print(action)
		reward = self.environment.make_step(action)
		new_state = self.environment.current_location
		print(new_state)
		agent.learn(old_state,reward, new_state,action)

	def textEdit_callback(self):
		self.inputNum+=1

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.pushButton.setText(_translate("MainWindow", "Start"))
		self.pushButton_2.setText(_translate("MainWindow", "End"))
		self.label.setText(_translate("MainWindow", "WPM:-"))
		self.label_2.setText(_translate("MainWindow", "IPM:-"))
		self.textEdit.setPlaceholderText('Click Start Button.')

class WorkThread(QThread):
	trigger = pyqtSignal(str)

	def __int__(self):
		super(WorkThread, self).__init__()

	def run(self):
		while 1:
			time.sleep(5)
			self.trigger.emit(str(1))
	

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
