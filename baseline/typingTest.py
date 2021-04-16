# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'typing.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.




from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import numpy as np
import operator
import matplotlib.pyplot as plt
import functools
# %matplotlib inline

class GridWorld:
    ## Initialise starting data
    def __init__(self):
        # Set information about the gridworld
        self.height = 1
        self.width = 5
        self.grid = np.zeros((self.height, self.width))
                
        # Set random start location for the agent
        self.current_location = (0,  np.random.randint(0,5))
        
        # Set locations for the bomb and the gold
        self.bomb_location = (0,0)
        self.gold_location = (0,4)
        self.terminal_states = [ self.bomb_location, self.gold_location]
        
        # Set grid rewards for special cells
        self.grid[ self.bomb_location[0], self.bomb_location[1]] = -10
        self.grid[ self.gold_location[0], self.gold_location[1]] = 10
        self.grid[0,1] = -8
        self.grid[0,2] = -5
        self.grid[0,3] = 5

        # Set available actions
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    
        
    ## Put methods here:
    def get_available_actions(self):
        """Returns possible actions"""
        return self.actions
    
    def agent_on_map(self):
        """Prints out current location of the agent on the grid (used for debugging)"""
        grid = np.zeros(( self.height, self.width))
        grid[ self.current_location[0], self.current_location[1]] = 1
        return grid
    
    def get_reward(self, new_location):
        """Returns the reward for an input position"""
        return self.grid[ new_location[0], new_location[1]]
        
    
    def make_step(self, action):
        """Moves the agent in the specified direction. If agent is at a border, agent stays still
        but takes negative reward. Function returns the reward for the move."""
        # Store previous location
        last_location = self.current_location

        

        a = 1
        if a == 1:
            if self.current_location[1] == 4:
                self.current_location = ( self.current_location[0], self.current_location[1])
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = ( self.current_location[0], self.current_location[1]+1)
                reward = self.get_reward(self.current_location)
        elif a == 0:
            self.current_location = ( self.current_location[0], self.current_location[1])
            reward = self.get_reward(self.current_location)
        else:
            if self.current_location[1] == 0:
                self.current_location = ( self.current_location[0], self.current_location[1])
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = ( self.current_location[0], self.current_location[1]-1)
                reward = self.get_reward(self.current_location)
        
#         # UP
#         if action == 'UP':
#             # If agent is at the top, stay still, collect reward
#             if last_location[0] == 0:
#                 reward = self.get_reward(last_location)
#             else:
#                 self.current_location = ( self.current_location[0] - 1, self.current_location[1])
#                 reward = self.get_reward(self.current_location)
        
#         # DOWN
#         elif action == 'DOWN':
#             # If agent is at bottom, stay still, collect reward
#             if last_location[0] == self.height - 1:
#                 reward = self.get_reward(last_location)
#             else:
#                 self.current_location = ( self.current_location[0] + 1, self.current_location[1])
#                 reward = self.get_reward(self.current_location)
            
#         # LEFT
#         elif action == 'LEFT':
#             # If agent is at the left, stay still, collect reward
#             if last_location[1] == 0:
#                 reward = self.get_reward(last_location)
#             else:
#                 self.current_location = ( self.current_location[0], self.current_location[1] - 1)
#                 reward = self.get_reward(self.current_location)

#         # RIGHT
#         elif action == 'RIGHT':
#             # If agent is at the right, stay still, collect reward
#             if last_location[1] == self.width - 1:
#                 reward = self.get_reward(last_location)
#             else:
#                 self.current_location = ( self.current_location[0], self.current_location[1] + 1)
#                 reward = self.get_reward(self.current_location)
                
        return reward
    
    def check_state(self):
        """Check if the agent is in a terminal state (gold or bomb), if so return 'TERMINAL'"""
        if self.current_location in self.terminal_states:
            return 'TERMINAL'

class RandomAgent():        
    # Choose a random action
    def choose_action(self, available_actions):
        """Returns a random choice of the available actions"""
        return np.random.choice(available_actions)   


class Q_Agent():
    # Intialise
    def __init__(self, environment, epsilon=0.05, alpha=0.1, gamma=1):
        self.environment = environment
        self.q_table = dict() # Store all Q-values in dictionary of dictionaries 
        for x in range(environment.height): # Loop through all possible grid spaces, create sub-dictionary for each
            for y in range(environment.width):
                self.q_table[(x,y)] = {'UP':0, 'DOWN':0, 'LEFT':0, 'RIGHT':0} # Populate sub-dictionary with zero values for possible moves

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        
    def choose_action(self, available_actions):
        """Returns the optimal action from Q-Value table. If multiple optimal actions, chooses random choice.
        Will make an exploratory random action dependent on epsilon."""
        if np.random.uniform(0,1) < self.epsilon:
            action = available_actions[np.random.randint(0, len(available_actions))]
        else:
            q_values_of_state = self.q_table[self.environment.current_location]
            maxValue = max(q_values_of_state.values())
            action = np.random.choice([k for k, v in q_values_of_state.items() if v == maxValue])
        
        return action
    
    def learn(self, old_state, reward, new_state, action):
        """Updates the Q-value table using Q-learning"""
        print(new_state)
        q_values_of_state = self.q_table[new_state]
        max_q_value_in_new_state = max(q_values_of_state.values())
        current_q_value = self.q_table[old_state][action]
        
        self.q_table[old_state][action] = (1 - self.alpha) * current_q_value + self.alpha * (reward + self.gamma * max_q_value_in_new_state)


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
		self.wpm=None #Word per minute
		self.ipm=None #Input per minute

	def startTest(self):
		self.textEdit.setPlaceholderText("")
		self.textEdit.setDisabled(False)
		self.work.start()
		self.startTime=time.time()
		environment = GridWorld()
		agentQ = Q_Agent(environment)
		update_call= functools.partial(self.updateInfo, environment=environment, agent = agentQ)
		self.work.trigger.connect(update_call)

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

		wpm=round((len(new_text)/5)/time_interval)
		ipm=round(self.inputNum/time_interval)

		# print(time_interval)
		# print(self.inputNum)
		# print(len(new_text))
		# print("----------")
		self.label.setText("WPM:"+str(wpm))
		self.label_2.setText("IPM:"+str(ipm))	

		old_state = environment.current_location
		action = agent.choose_action(environment.actions)
		reward = environment.make_step(action)
		print(reward)
		new_state = environment.current_location
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
			time.sleep(1)
			self.trigger.emit(str(1))
	


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())