from electric_sheep.hexagon import *
from electric_sheep.player import *
import random



FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}

class Strategy:
    def __init__(self):
        return

    def get_next_move(self, player):
        availbe_actions = self.all_valid_actions(player)
        if len(availbe_actions) == 0:
            move = ("PASS", None)
        else:
            move = random.choice(availbe_actions)
        return move


    def all_valid_actions(self,player):
        valid_moves = []
        for piece in player.pieces:
            if piece in FINISHING_HEXES[player.colour]:
                new_move = ("EXIT", piece)
                valid_moves.append(new_move)
            for move in MOVE_ACTIONS:
                #find new positon
                new_pos = numpy.add(piece, move)
                if player.board.is_valid_position(new_pos):
                    #make MOVE action
                    if player.board.hexagon_dict[tuple(new_pos)].occupant == "e":
                        new_move = ("MOVE", (piece, tuple(new_pos)))
                        valid_moves.append(new_move)
                    else:
                        #make JUMP action
                        new_pos = numpy.add(tuple(new_pos), move)
                        if player.board.is_valid_position(new_pos) and player.board.hexagon_dict[tuple(new_pos)].occupant == "e":
                            new_move = ("JUMP", (piece, tuple(new_pos)))
                            valid_moves.append(new_move)
        return valid_moves
