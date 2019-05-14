from randomP.hexagon import *
from randomP.player import *

FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}

class Strategy:
    def __init__(self):
        return


    def get_next_move(self, player):
        move = ("PASS", None)
        return move