import numpy as np
import operator
import matplotlib.pyplot as plt
import pygame as pg

class RandomAgent():        
    # Choose a random action
    def choose_action(self, available_actions):
        """Returns a random choice of the available actions"""
        return np.random.choice(available_actions)   

class MAB_Agent():
    # Intialize
    def __init__(self, algorithm):
        self.algorithm = algorithm # Different MAB algorithm has different initialization function, go to algorithm folder to check init()
        
    def select_arm(self):
        """Returns the current 'best' action from arms. If multiple optimal actions, chooses random choice."""
        
        actionIndex=self.algorithm.select_arm()
        self.give_feedback(actionIndex) # Current way is play audio feedback
        return actionIndex
    
    def update(self, chosen_arm, reward):
        """Updates the arms' values"""
        self.algorithm.update(chosen_arm, reward)

    def reset(self):
        """Reset the agent's algorithm"""
        self.algorithm.reset()

    def give_feedback(self, actionIndex):
        """According to selected arm, MAB_Agent give feedback(only audio right now)
        """
        if actionIndex == 0:
            pg.mixer.music.load('audio/0.mp3')
        elif actionIndex == 1:
            pg.mixer.music.load('audio/1.mp3')
        elif actionIndex == 2:
            pg.mixer.music.load('audio/2.mp3')
        elif actionIndex == 3:
            pg.mixer.music.load('audio/3.mp3')
        elif actionIndex == 4:
            pg.mixer.music.load('audio/4.mp3')
        elif actionIndex == 5:
            pg.mixer.music.load('audio/5.mp3')
        elif actionIndex == 6:
            pg.mixer.music.load('audio/6.mp3')
        elif actionIndex == 7:
            pg.mixer.music.load('audio/7.mp3')
        elif actionIndex == 8:
            pg.mixer.music.load('audio/8.mp3')
        elif actionIndex == 9:
            pg.mixer.music.load('audio/9.mp3')
        pg.mixer.music.play()
