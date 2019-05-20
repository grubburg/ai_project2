# module containing all global constants and functions
# that relate to the rules of the game

ALL_COLOUR = ["red", "green", "blue"]

FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}

RED_START = ((-3,3), (-3,2), (-3,1), (-3,0))
GREEN_START = ((0,-3), (1,-3), (2,-3), (3,-3))
BLUE_START = ((3, 0), (2, 1), (1, 2), (0, 3))

VALID_TILES = [(q, r) for q in range(-3,4) for r in range(-3,4) if -q - r in range(-3,4)]

INF = 100000000

EMPTY = "e"

PASS = ('PASS', None)

MOVE_ACTIONS = [[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]]

def is_valid_position(positon):
    if tuple(positon) in VALID_TILES:
        return True
    else:
        return False