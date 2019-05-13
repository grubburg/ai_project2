from electric_sheep.board import *

FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}

ALL_COLOUR = ["red", "green", "blue"]

INF = 100000000

class Strategy:
    def __init__(self, state):
        self.state = state


    def get_next_move(self, colour):
        """
        Function to return the next move the player should make.
        Employs 'best reply search' defined in brs()
        :param current_state:
        :param colour:
        :return:
        """
        moves = self.state.get_successor_states()

        best_score = -INF

        best_move = None
        for move in moves:
            move_score = move.brs(-INF, INF, 5, True)
            if move_score > best_score:
                best_move = move
                best_score = move_score

        return best_move.arrived_by_move






class State:

    def __init__(self, board, colour, arrived_by_move):
        self.positions = board.position_dict
        self.colour = colour
        self.arrived_by_move = arrived_by_move

    def eval(self):
        return 0

    def make_move(self, move):
        return 0
    def unmake_move(self, move):
        return 0
    def get_all_moves(self, colour):

        return 0

    def get_successor_states(self):
        return 0

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
            # if it is our turn, find all our moves
            moves = self.get_all_moves(self.colour)
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
            # apply a move to the current state
            self.make_move(move)
            #
            v = -self.brs(-a, -b, depth-1, turn)
            self.unmake_move(move)

            if v > b:
                return v
            a = max(a, v)

        return a





