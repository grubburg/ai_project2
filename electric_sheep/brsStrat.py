from electric_sheep.board import *
from copy import deepcopy
import numpy

FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}

ALL_COLOUR = ["red", "green", "blue"]

VALID_TILES = [(q, r) for q in range(-3,4) for r in range(-3,4) if -q - r in range(-3,4)]

INF = 100000000

class State:

    def __init__(self, position_dict, score, arrive_by_move):
        self.position_dict = position_dict
        self.score = score
        self.arrived_by_move = arrive_by_move


    def successor_states(self, colour):

        states = []
        for piece in self.position_dict[colour]:
            if piece in FINISHING_HEXES[colour]:

        return None

    def get_all_moves(self, colour):

        valid_moves = []
        for piece in tuple(self.position_dict[colour]):
            if piece in FINISHING_HEXES[colour]:
                new_move = ("EXIT", piece)
                valid_moves.append((new_move, colour))
            for move in MOVE_ACTIONS:
                # find new positon
                new_pos = numpy.add(piece, move)
                if new_pos in VALID_TILES:
                    # make MOVE action

                    for other_colour in [c for c in ALL_COLOUR if c != colour]:
                        if new_pos not in self.position_dict[other_colour]:
                            new_move = ("MOVE", (piece, tuple(new_pos)))
                            valid_moves.append((new_move, colour))
                        else:
                            # make JUMP action
                            new_pos = numpy.add(tuple(new_pos), move)
                            if self.board.is_valid_position(new_pos) and self.board.hexagon_dict[

                                tuple(new_pos)].occupant == "e":
                                new_move = ("JUMP", (piece, tuple(new_pos)))
                                valid_moves.append((new_move, colour))
        return valid_moves


class Strategy:

    def __init__(self, board, colour, arrived_by_move, score):
        self.board = board
        self.positions = board.position_dict
        self.colour = colour
        self.arrived_by_move = arrived_by_move
        self.score = score

    def get_next_move(self):
        """
        Function to return the next move the player should make.
        Employs 'best reply search' defined in brs()
        """
        moves = self.get_successor_states()

        best_score = -INF

        best_move = None
        for move in moves:
            # print(move.arrived_by_move)
            move_score = -move.brs(INF, -INF, 3, True)
            if move_score >= best_score:
                best_move = move
                best_score = move_score

        print(best_score)

        return best_move.arrived_by_move



    def eval(self):
        pieces = self.positions[self.colour]
        num_pieces = len(pieces)+1
        dist_count = 0
        for pos in pieces:
            dist_count += self.board.path_costs[pos]
        avg_dist = dist_count/num_pieces
        return -5*avg_dist + 2*num_pieces + 10*self.score



    def make_move(self, move, colour):



        if move[0] == "JUMP":
            # find jumped over piece
            middle_piece = tuple(numpy.add(move[1][0], move[1][1]) / 2)

            self.positions[colour].remove(move[1][0])
            self.positions[colour].append(move[1][1])
            if middle_piece not in self.positions[colour]:
                for player in [c for c in ALL_COLOUR if c != colour]:
                    if middle_piece in self.positions[player]:
                        self.positions[player].remove(middle_piece)
                        self.positions[colour].append(middle_piece)
            

        elif move[0] == "MOVE":
            self.positions[colour].remove(move[1][0])
            self.positions[colour].append(move[1][1])

            
        elif move[0] == "EXIT":
            self.positions[colour].remove(move[1])
            self.score += 1



    def unmake_move(self, move):
        return 0



    def get_successor_states(self):
        state_array = []
        for move in self.get_all_moves(self.colour):
            new_state = Strategy(deepcopy(self.board), self.colour, move[0], self.score)
            new_state.make_move(move[0], self.colour)
            state_array.append(new_state)
        return state_array



    def brs(self, a, b, depth, turn):
        """
        Implementation of 'best reply search, where only
        a single move made by the most threatening enemy is
        considered in an a-b search through the search space.

        We specify a b, initially -inf +inf respectively, search
        depth d, and whether or not it is our turn. brs is then
        called recursively.
        """
        if depth <= 0:
            # if we reach the specified depth, return the value of the board at this point
            return self.eval()

        if turn:

            v = -INF
            # if it is our turn, find all our moves

            moves = self.get_all_moves(self.colour)
            for move in moves:
                self.make_move(move[0], move[1])
                v = self.brs,
            # set the next turn to NOT our turn
            turn = False
        else:





            # otherwise find all possible opponent moves
            moves = []
            for opponent in [c for c in ALL_COLOUR if c != self.colour]:
                moves += self.get_all_moves(opponent)
            # set the next turn to our turn
            turn = True


        for move in moves:
            current_state = deepcopy(self.positions)
            current_score = self.score
            # apply a move to the current state
            self.make_move(move[0], move[1])
            #
            v = -self.brs(-a, -b, depth-1, turn)
            # self.unmake_move(move)
            self.positions = current_state
            self.score = current_score
            if v >= b:
                return v
            a = max(a, v)

        return a




def cubify(pos):
    return (pos[0], pos[1], -pos[0]-pos[1])

def euclidian_distance(action, exit_pos):
    cube_action = cubify(action)
    cube_exit = cubify(exit_pos)
    distance = (cube_action[0] - cube_exit[0])**2 + (cube_action[1] - cube_exit[1])**2 + (cube_action[2] - cube_exit[2])**2
    return distance