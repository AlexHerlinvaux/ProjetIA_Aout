from player import Player
import random
import itertools
import numpy as np

class IA(Player):
    def __init__(self, id_player, oX, oY, epsilon = 0.99, lr = 0.0000001, dr = 0.0000001, trainable = True):
        Player.__init__(self, id_player, (oX, oY))
        self._epsilon = epsilon
        self._lr = lr #Learning Rate
        self._dr = dr #Discount Rate
        self._trainable = trainable
        self._Q = {}
        self._history = []
	
    @property
    def epsilon(self):
        return self._epsilon
    
    @epsilon.setter
    def epsilon(self, new_eps):
        self._epsilon = new_eps
		
    @property
    def lr(self):
        return self._lr
    
    @lr.setter
    def lr(self, new_lr):
        self._lr = new_lr
		
    @property
    def dr(self):
        return self._dr
    
    @dr.setter
    def dr(self, new_dr):
        self._dr = new_dr
	
    @property
    def is_trainable(self):
        return self._trainable
    
    @property
    def Q(self):
        return self._Q
    
    @Q.setter
    def Q(self, new_Q):
        self._Q = new_Q
        
    def add_transition(self, step):
        self._history.append(step)
        
    def update_transition(self, transition, id_transition=-1):
        self._history[id_transition] = transition
        
    def get_transition(self, id_transition=-1):
        return self._history[id_transition]
    
    def print_history(self):
        print(self._history)
        
    def translate(self, direction) :
        if direction == "up" :
            return 0
        if direction == "down" :
            return 1
        if direction == "right" :
            return 2
        else :
            return 3

    
    def training(self, id_ia):
        if self.is_trainable:
            for i, transition in enumerate(reversed(self._history)):
                action,s,sp,r = transition
                if (not str(s) in self.Q.keys()):
                    self._Q[str(s)] = [0,0,0,0]
                    
                if (str(sp) is not None and not str(sp) in self.Q.keys()):
                    self._Q[str(sp)] = [0,0,0,0]
                    
                if (i != 0):
                    action_index = self.translate(action)
                    max_prime = max(self._Q[str(sp)])
                    self._Q[str(s)][action_index] += self._lr * (r + self._dr * (max_prime - self._Q[str(s)][action_index]))
      
    def play(self, game):
        possible_action=["up","down","right","left"]
        if random.uniform(0,1) < self.epsilon :
            action = random.choice(possible_action) #Exploration
        else:
            move, s, sp, r = self.get_transition()
            if str(sp) in self._Q :
                action = max(self.Q[str(sp)])
            else : 
                action = random.choice(possible_action)
        return action