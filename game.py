from player import Player
from copy import deepcopy
import numpy as np

class Game :
    def __init__(self, player1, player2, size_matrix) :
        self._board = []
        self._players = [player1, player2]
        self._turn = 0
        self._state = 0
        self._size = size_matrix
        self._nb_cells = size_matrix * size_matrix
        self._nb_cells_left = self._nb_cells
        
        @property
        def state(self):
            return self._state
    
        @property
        def board(self):
            return self._board 
    
        @property
        def players(self):
            return self._players
    
        @property
        def size(self):
            return self._size
    
        @property
        def turn(self):
            return self._turn
        
    def init_board(self):
        self._board = [[0 for col in range(0,self._size)] for row in range(0,self._size)]
    
    def is_valid_coord(self, x,y) :
        return ((x >= 0 and x < self._size) and (y >= 0 and y < self._size))
    
    def get_cell(self, coord) :
        x,y = coord
        if self.is_valid_coord(x,y):
            return self._board[x][y]
    
    def update_cell(self, coord, player):
        x,y = coord
        current_value = self.get_cell(coord)
        if current_value == 0 :
            self._board[x][y] = player._id
            player._points += 1
            self._nb_cells_left -= 1
    
    def fill_cases_tmp(self, init_coord, cases_tmp, player) :
        x, y = init_coord
        if x - 1 >= 0 and cases_tmp[x-1][y] != player._id :
                cases_tmp[x-1][y] = player._id
                cases_tmp = self.fill_cases_tmp((x-1,y), cases_tmp, player)
        if x + 1 < self._size and cases_tmp[x+1][y] != player._id :
                cases_tmp[x+1][y] = player._id
                cases_tmp = self.fill_cases_tmp((x+1,y), cases_tmp, player)
        if y - 1 >= 0 and cases_tmp[x][y-1] != player._id :
                cases_tmp[x][y-1] = player._id
                cases_tmp = self.fill_cases_tmp((x,y-1), cases_tmp, player)
        if y + 1 < self._size and cases_tmp[x][y+1] != player._id :
                cases_tmp[x][y+1] = player._id
                cases_tmp = self.fill_cases_tmp((x,y+1), cases_tmp, player)
            
        return cases_tmp
            
    def shape_detection(self, coord, player):
        cases_tmp = deepcopy(self._board)
        
        if player._id == 2 :
            cases_tmp = self.fill_cases_tmp((self._size-1,self._size-1),cases_tmp, player)
        else :
            cases_tmp = self.fill_cases_tmp((0,0),cases_tmp, player)
        
        for i in range(self._size):
            for j in range(self._size):
                if cases_tmp[i][j] == 0:
                    self.update_cell((i,j),player)
                    
    def draw_cell(self, coord, player):
        self.update_cell(coord, player)
        self.shape_detection(coord, player)
    
    def start(self):
        self.init_board()
        self.update_cell((0,0), self._players[0])
        self.update_cell((self._size-1, self._size-1), self._players[1])
        self._state = 1
        
    def is_valid_action(self, coord, player):
        x,y = coord
        if not self.is_valid_coord(x,y):
            return False
        if not (self.get_cell(coord) == player._id or self.get_cell(coord) == 0) :
            return False
        return True
        
    def get_winner(self):
        if self.players[0]._points > self.players[1]._points:
            return self._players[0].id
        return self.players[1]._id
    
    def play_turn(self, direction):
        if self._state != 1:
            return 0
        
        reward = 0
        player = self._players[self._turn]
        new_coord = player.move(direction)
        if self.is_valid_action(new_coord, player):
            player.current_coord = new_coord
            self.draw_cell(new_coord, player)
        if self._nb_cells_left <= 0:
            self._state = 2
        reward = player._points - self._players[(self._turn+1)%2]._points
        
        self._turn = (self._turn+1)%2
        return reward
    
    def draw_board(self):
        board_print = ""
        for i in range(0,self.size):
            for j in range(0,self.size):
                board_print += str(self.get_cell((i,j))) + " "
            board_print += "\n"
    
    def restart(self):
        self.init_board()
        self._nb_cells_left = self._nb_cells
        self._turn = 0
        self._state = 0
        self._players[0].reset_player()
        self._players[1].reset_player()
