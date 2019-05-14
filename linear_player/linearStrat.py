from linear_player.hexagon import *
from linear_player.player import *

"""
A linear implementation of a partially paranoid player
uses static hueristic, to stay group together and avoid enemy
very passive
"""

FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}

class Strategy:
    def __init__(self):
        return


    def get_next_move(self, player):
        all_valid = self.all_valid_actions(player)
        if len(all_valid) == 0:
            move = ("PASS", None)
        else:
            min_score = None
            move = None
            for action in all_valid:
                curr_eval = self.eval_action(action, player)
                if min_score == None or curr_eval < min_score:
                    min_score = curr_eval
                    move = action
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


    #aim is to minimize the score 
    def eval_action(self, action, player):
        score = 0
        if action[0] == "EXIT":
            return score

        #add euclidian distance modifier
        for exit_pos in FINISHING_HEXES[player.colour]:
            score += euclidian_distance(action[1][1], exit_pos)
        score = score//4

        if action[0] == "JUMP":
            score += 5
        #add safety modifier
        for neighbour in player.board.hexagon_dict[action[1][1]].neighbours:
            #if close to other friendlies
            if player.board.hexagon_dict[neighbour].occupant == player.colour and neighbour != action[1][0]:
                score -= 10
            #if close to enemies
            elif player.board.hexagon_dict[neighbour].occupant != "e":
                score += 10

            #non-group danger
            else:
                score += 5
        return score


def cubify(pos):
    return (pos[0], pos[1], -pos[0]-pos[1])

def euclidian_distance(action, exit_pos):
    cube_action = cubify(action)
    cube_exit = cubify(exit_pos)
    distance = (cube_action[0] - cube_exit[0])**2 + (cube_action[1] - cube_exit[1])**2 + (cube_action[2] - cube_exit[2])**2
    return distance