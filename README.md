# Learning How to Re-Engage 

##### This repository was made to facilitate the development of a socially intelligent assistive robot that is capable of learning how to re-engage user in a socially appropriate and personalized fashion.

## Usage

### Installation
```
1. Create and activate a virtual machine using Anaconda with python version as 3.9.4 (Anaconda virtual environment tutorial can be found here: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) 
2. git clone git@github.com:HaaaO/re-engagement-RL.git
3. cd re-engagement-RL
4. pip3 install -r requirements.txt
```

### Running the current script
```
1. Run python3 typingTest.py. Test begins when 'start' button is clicked.
```

### Understanding the script for learning-how-to-reengage-typingTest.py
```
1. Ui_MainWindow.starttest() is run when 'start' button is clicked. 
2. Ui_MainWindow.getWPMandIPM() calculates and returns WPM and IPM. This is run every second (second-by-second recording is regulated by RecordWorkThread(QThread)). 
3. self.log keeps track of time in seconds that the program has been running, wpm, and ipm. A record of this is saved onto 'test.csv' when the program finishes.
```

### Understanding the script for learning-how-to-reengage-typingTest.py
```
1. Contains all the functionality of learning-how-to-reengage-typingTest.py.
2. Uses EpsilonGreedy.py (a Multi-Armed Bandit Algorithm) to choose a re-engagement feedback, which plays every 15 seconds. This is controlled through playAudio(self, agent) in typingTest.py, environment.py, and EpsilonGreedy.py.
```
