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
import numpy as np
# %matplotlib inline


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(692, 477)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
		font = QtGui.QFont()
		font.setPointSize(14)
		self.textEdit.setFont(font)
		self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.textEdit.setObjectName("textEdit")
		self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setObjectName("pushButton")
		self.horizontalLayout.addWidget(self.pushButton)
		self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_2.setObjectName("pushButton_2")
		self.horizontalLayout.addWidget(self.pushButton_2)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_3.setStyleSheet("border:none; background-color: gray")
		self.pushButton_3.setEnabled(False)
		self.pushButton_3.setObjectName("pushButton_3")
		self.horizontalLayout.addWidget(self.pushButton_3)
		self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_4.setStyleSheet("border:none; background-color: gray")
		self.pushButton_4.setEnabled(False)
		self.pushButton_4.setObjectName("pushButton_4")
		self.horizontalLayout.addWidget(self.pushButton_4)
		self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
		self.pushButton_5.setSizePolicy(sizePolicy)
		self.pushButton_5.setStyleSheet("border:none; background-color: gray")
		self.pushButton_5.setEnabled(False)
		self.pushButton_5.setObjectName("pushButton_5")
		self.horizontalLayout.addWidget(self.pushButton_5)
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setObjectName("label")
		self.horizontalLayout.addWidget(self.label)
		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setObjectName("label_2")
		self.horizontalLayout.addWidget(self.label_2)
		self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
		self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		self.pushButton.clicked.connect(self.startTest)
		self.pushButton_2.clicked.connect(self.resetTest)
		self.pushButton_3.clicked.connect(self.getNegativeReward)
		self.pushButton_4.clicked.connect(self.getNormalReward)
		self.pushButton_5.clicked.connect(self.getPositiveReward)

		self.textEdit.textChanged.connect(self.textEdit_callback)
		self.textEdit.setDisabled(True)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		#Added code here
		self.recordWork = RecordWorkThread() #Work Thread
		self.qlearningWork = QLearningWorkThread() 
		self.startTime=None
		self.inputNum=0 #All keyboard inputNum
		self.inputNumLast = 0
		self.wpm=None #Word per minute
		self.ipm=None #Input per minute
		self.allInputNum=[]
		self.validInputNum=[]
		self.action='None'

		self.reward_record = []
		self.human_reward_record = []
		self.humanRewardFeedback=0

	def startTest(self):
		self.allInputNum=[]
		self.validAlphaNum=[]
		self.textEdit.setPlaceholderText("")
		self.textEdit.setDisabled(False)
		self.recordWork.start()
		self.qlearningWork.start()
		self.environment = environment.GridWorld()
		self.agentQ = agent.Q_Agent(self.environment)
		self.update_call= functools.partial(self.updateInfo, environment=self.environment, agent = self.agentQ)
		pg.mixer.init()
		self.recordWork.recordTrigger.connect(self.recordInputInfo)
		self.qlearningWork.qlearningTrigger.connect(self.update_call)

		# Start timer
		self.startTime=time.time()

	def resetTest(self):
		self.allInputNum=[]
		self.validAlphaNum=[]
		self.inputNum=0
		self.textEdit.setPlainText("")
		self.textEdit.setDisabled(True)
		self.label.setText("WPM:-")
		self.label_2.setText("IPM:-")
		np.savetxt("reward.csv", np.array(self.reward_record), delimiter=",")
		np.savetxt("human_rward.csv", np.array(self.human_reward_record), delimiter=",")

	def recordInputInfo(self):
		#Calculate time interval
		time_interval=(time.time()-self.startTime)/60

		#Just keep characters from textEdit
		text=self.textEdit.toPlainText()
		temp=filter(str.isalpha, text)
		new_text=''.join(list(temp))
		print(new_text)

		#Suppose after sleep(1), these two lists will append the number of 1,2,3,4,5 seconds.
		#I mean this may not very accurate.
		self.allInputNum.append(self.inputNum)
		self.validAlphaNum.append(len(new_text))

		timeIs=len(self.allInputNum)
		wpm,ipm=self.getWPMandIPM(timeIs,5)

		#test github
		self.label.setText("WPM:"+str(wpm))	
		self.label_2.setText("IPM:"+str(ipm))

		self.wpm=wpm
		self.ipm=ipm


	def updateInfo(self, environment, agent):
		# get old state
		old_state = self.environment.current_location

		old_action = self.action

		self.environment.current_location = self.getCurrentLocation()

		self.action = agent.choose_action(self.environment.actions)

		reward = self.environment.make_step(self.action)

		print(self.pushButton_3.isEnabled())
		if self.pushButton_3.isEnabled():
			self.humanRewardFeedback=0.5

		self.activateButton()

		self.reward_record.append(reward)
		print(self.humanRewardFeedback)
		self.human_reward_record.append(self.humanRewardFeedback)
		agent.learn(old_state, reward, self.humanRewardFeedback, self.environment.current_location, old_action)

	def activateButton(self):
		self.pushButton_3.setEnabled(True)
		self.pushButton_4.setEnabled(True)
		self.pushButton_5.setEnabled(True)
		self.pushButton_3.setStyleSheet("border:none; background-color: red")
		self.pushButton_4.setStyleSheet("border:none; background-color: yellow")
		self.pushButton_5.setStyleSheet("border:none; background-color: green")

	def disableButton(self):
		self.pushButton_3.setEnabled(False)
		self.pushButton_4.setEnabled(False)
		self.pushButton_5.setEnabled(False)
		self.pushButton_3.setStyleSheet("border:none; background-color: gray")
		self.pushButton_4.setStyleSheet("border:none; background-color: gray")
		self.pushButton_5.setStyleSheet("border:none; background-color: gray")		

	def getCurrentLocation(self):
		new_state=None
		if self.wpm<=2:
			new_state=(0,0)
		elif self.wpm>2 and self.wpm<=4:
			new_state=(0,1)
		elif self.wpm>4 and self.wpm<=6:
			new_state=(0,2)
		elif self.wpm>6 and self.wpm<=8:
			new_state=(0,3)		
		else:
			new_state=(0,4)	
		
		return new_state

	def getWPMandIPM(self,time,interval):
		"""Given time t, and time interval, we calculate the wpm and ipm
		"""
		if time <= interval:
			wpm=round(self.validAlphaNum[time-1]/(time/60))
			ipm=round(self.allInputNum[time-1]/(time/60))
		else:
			wpm=round((self.validAlphaNum[time-1]-self.validAlphaNum[time-1-interval])/(interval/60))
			ipm=round((self.allInputNum[time-1]-self.allInputNum[time-1-interval])/(interval/60))
		
		return wpm,ipm

	def textEdit_callback(self):
		self.inputNum+=1

	def getNegativeReward(self):
		self.humanRewardFeedback=-5
		self.disableButton()

	def getNormalReward(self):
		self.humanRewardFeedback=0
		self.disableButton()

	def getPositiveReward(self):
		self.humanRewardFeedback=5
		self.disableButton()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Typing"))
		self.pushButton.setText(_translate("MainWindow", "Start"))
		self.pushButton_2.setText(_translate("MainWindow", "End"))

		self.pushButton_3.setText(_translate("MainWindow", ""))
		self.pushButton_4.setText(_translate("MainWindow", ""))
		self.pushButton_5.setText(_translate("MainWindow", ""))

		self.label.setText(_translate("MainWindow", "WPM:-"))
		self.label_2.setText(_translate("MainWindow", "IPM:-"))
		self.textEdit.setPlaceholderText('Click Start Button.')

#For recording input info once per second
class RecordWorkThread(QThread):
	recordTrigger = pyqtSignal(str)

	def __int__(self):
		super(RecordWorkThread, self).__init__()

	def run(self):
		while 1:
			time.sleep(1)
			self.recordTrigger.emit(str(1))

#For updating Qagent per once per 30 seconds
class QLearningWorkThread(QThread):
	qlearningTrigger = pyqtSignal(str)

	def __int__(self):
		super(QLearningWorkThread, self).__init__()

	def run(self):
		while 1:
			time.sleep(5)
			self.qlearningTrigger.emit(str(1))

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())



