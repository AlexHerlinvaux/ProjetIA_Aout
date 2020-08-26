from game import Game
from player import Player
from ia import IA
from datetime import datetime
from copy import deepcopy
import pickle
import os

DEFAULT_SIZE = 4

def play(game, training = True):
    game.restart()
    game.start()
    turn = 0
    players = game._players
    st = game._board
    while(game._state != 2):
        action = None
        if not isinstance(players[game._turn], IA):
            game.draw_board()
            action = players[game._turn].play()
        else:
            action = players[game._turn].play(game)
        reward = game.play_turn(action)
        new_st = game._board
        if training:
            if(turn != 0 and turn !=1 ):
                if isinstance(players[(game._turn+1)%2], IA):
                    a,s,sp,r = players[(game._turn + 1)%2].get_transition()
                    players[(game._turn + 1)%2].add_transition((deepcopy(action),deepcopy(sp), deepcopy(new_st), deepcopy(reward*-1)))
            else:
                if isinstance(players[game._turn], IA):
                    players[game._turn].add_transition((deepcopy(action),deepcopy(st), None, deepcopy(reward)))
        turn += 1
        st = new_st
    
    if isinstance(players[game._turn], IA):
        players[game._turn].training(game._turn)
    if isinstance(players[(game._turn + 1 )%2], IA):
        players[(game._turn + 1)%2].training((game._turn + 1)%2)
        
def training_ai(ai1_Q = {}, ai2_Q = {}, n = 10000):
    ai1 = IA("1", 0,0)
    ai2 = IA("2",DEFAULT_SIZE - 1,DEFAULT_SIZE - 1)
    ai1._Q = ai1_Q
    ai2._Q = ai2_Q
    players_g1 = [ai1, ai2]
    game = Game(ai1, ai2, DEFAULT_SIZE)
    for i in range(n):
        print(i)
        if i % 1000 == 0:
            print("%s - %d " % (datetime.now(tz=None), i))

        if(i % 1000 == 0):
            players_g1[0]._epsilon = max(players_g1[0]._epsilon * 0.996, 0.05)
            players_g1[1]._epsilon = max(players_g1[1]._epsilon * 0.996, 0.05)
        
        play(game)
    return ai1._Q
 
def play_human(ai_q = {}):   
    ai1 = IA("1", 0,0, epsilon=0)
    ai1.Q = ai_q
    p1 = Player("2", DEFAULT_SIZE - 1,DEFAULT_SIZE - 1)
    game = Game(ai1, p1, DEFAULT_SIZE)
    while True:
        play(game, train=False)

if __name__ == "__main__":
    if os.path.exists("ai_data.dat"):
        ai_Q = pickle.load(open("ai_data.dat", "rb"))
        train = input("train ? (y/n)") == 'y'
        if train:
            ai_Q = training_ai(ai1_Q = ai_Q)
            pickle.dump(ai_Q, open("ai_data.dat", "wb"))
        else:
            play_human(ai_Q = ai_Q)
        
    else:
        ai = training_ai()
        pickle.dump(ai, open("ai_data.dat", "wb"))
        play_human(ai)
