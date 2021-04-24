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
		self.work.quit()
		self.allInputNum=[]
		self.validAlphaNum=[]
		self.inputNum=0
		self.textEdit.setPlainText("")
		self.textEdit.setDisabled(True)
		self.label.setText("WPM:-")
		self.label_2.setText("IPM:-")

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

		human_reward = self.get_human_reward()

		agent.learn(old_state, reward, human_reward, self.environment.current_location, old_action)



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
			wpm=round(self.validAlphaNum[time-1]/time)
			ipm=round(self.allInputNum[time-1]/time)
		else:
			wpm=round((self.validAlphaNum[time-1]-self.validAlphaNum[time-1-interval])/interval)
			ipm=round((self.allInputNum[time-1]-self.allInputNum[time-1-interval])/interval)
		
		return wpm,ipm

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
