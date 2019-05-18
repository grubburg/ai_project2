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
    """
    Maintains a representation of the state of the game at a given stage.
    Tracks positions of all pieces, scores of all players, and the move
    that was made to arrive at the given state.
    """
    def __init__(self, position_dict, score_dict, arrive_by_move):
        self.position_dict = position_dict
        self.score_dict = score_dict
        self.arrived_by_move = arrive_by_move

    def successor_states(self, colour):
        """
        Method to return all the states that result from a move made by the player 'colour'
        States are returned as an array of states.
        :param colour: the player moving
        :return: array of states that result from those moves
        """
        child_states = []

        moves = self.get_all_moves(colour)


        for move in moves:
            # generate states resulting from exit move
            if move[0] == "EXIT":
                # update position information
                new_position_dict = deepcopy(self.position_dict)
                new_position_dict[colour].remove(move[1])
                # update score information
                new_score_dict = deepcopy(self.score_dict)
                new_score_dict[colour] += 1
                new_state = State(new_position_dict, new_score_dict, move)
                child_states.append(new_state)

            if move[0] == "MOVE":
                # update position information
                new_position_dict = deepcopy(self.position_dict)
                new_position_dict[colour].remove(move[1][0])
                new_position_dict[colour].append(move[1][1])

                new_state = State(new_position_dict, self.score_dict, move)
                child_states.append(new_state)

            if move[0] == "JUMP":
                # update position information
                new_position_dict = deepcopy(self.position_dict)
                middle_piece = tuple(numpy.add(move[1][0], move[1][1]) / 2)
                new_position_dict[colour].remove(move[1][0])
                new_position_dict[colour].append(move[1][1])

                for other_colour in [c for c in ALL_COLOUR if c != colour]:
                    if middle_piece in new_position_dict[other_colour]:
                        new_position_dict[other_colour].remove(middle_piece)
                        new_position_dict[colour].append(middle_piece)
                new_state = State(new_position_dict, self.score_dict, move)
                child_states.append(new_state)

        return child_states

    def get_all_moves(self, colour):
        """
        Method to return all moves that can be made by a given player.
        :param colour: the player whos moves we are finding
        :return: a list of moves that can be made by the player
        """
        valid_moves = []
        if len(self.position_dict[colour]) > 0:
            for piece in tuple(self.position_dict[colour]):
                if piece in FINISHING_HEXES[colour]:
                    new_move = ("EXIT", piece)
                    valid_moves.append(new_move)
                for move in MOVE_ACTIONS:
                    # find new position
                    new_pos = tuple(numpy.add(piece, move))

                    if new_pos in VALID_TILES:
                        # make MOVE action

                        all_pieces = []
                        for c in ALL_COLOUR:
                            all_pieces += self.position_dict[c]

                        if new_pos not in all_pieces:
                            new_move = ("MOVE", (piece, tuple(new_pos)))
                            valid_moves.append(new_move)

                        else:
                            new_pos = tuple(numpy.add(tuple(new_pos), move))
                            if new_pos not in all_pieces and new_pos in VALID_TILES:
                                new_move = ("JUMP", (piece, tuple(new_pos)))
                                valid_moves.append((new_move))
        else:
            # if the player has no pieces, return only the pass move
            return [("PASS", None)]



        return valid_moves

    def make_move(self, move, colour):

        if move[0] == "JUMP":
            # find jumped over piece
            middle_piece = tuple(numpy.add(move[1][0], move[1][1]) / 2)

            self.position_dict[colour].remove(move[1][0])
            self.position_dict[colour].append(move[1][1])
            if middle_piece not in self.position_dict[colour]:
                for player in [c for c in ALL_COLOUR if c != colour]:
                    if middle_piece in self.position_dict[player]:
                        self.position_dict[player].remove(middle_piece)
                        self.position_dict[colour].append(middle_piece)


        elif move[0] == "MOVE":
            self.position_dict[colour].remove(move[1][0])
            self.position_dict[colour].append(move[1][1])


        elif move[0] == "EXIT":
            self.position_dict[colour].remove(move[1])
            self.score_dict[colour] += 1

class Strategy:

    def __init__(self, state, colour, cost_dict):
        self.state = state
        self.colour = colour
        self.cost_dict = cost_dict

    def get_next_move(self):
        """
        Function to return the next move the player should make.
        Employs 'best reply search' defined in brs()
        """
        best_score = -INF
        best_move = ("PASS", None)

        for child in self.state.successor_states(self.colour):

            current_score = self.brs(child, -INF, INF, 2, True)

            if current_score > best_score:
                best_score = current_score
                best_move = child.arrived_by_move

        if best_move[0] == "EXIT":
            return (best_move[0], (int(best_move[1][0]), int(best_move[1][1])))

        elif best_move[0] == "JUMP" or best_move[0] == "MOVE":
            return (best_move[0], ((int(best_move[1][0][0]), int(best_move[1][0][1])),
                                  (int(best_move[1][1][0]), int(best_move[1][1][1]))))
        else:
            return ("PASS", None)


    def brs(self, state, a, b, depth, turn):
        """
        Implementation of 'best reply search'. Similar to a-b minimax,
        except only the best move by any opponent is considered.
        :param state: the state to return an evaluation for
        :param a:
        :param b:
        :param depth: the depth to search to
        :param turn: whether or not it is the root players turn
        :return: an evaluation of 
        """

        # note: need to include condition for terminal node.
        if depth <= 0:
            return eval_state(state, self.colour, self.cost_dict)
        # if it is the root players turn
        if turn:
            #initialise the value to negative infinity
            v = -INF
            # find all states emanating from root player's actions
            for child in state.successor_states(self.colour):

                v = max(v, self.brs(child, a, b, depth-1, False))
                a = max(a, v)
                if a > b:
                    break
            return v

        else:
            v = INF
            child_states = []
            for other_colour in [c for c in ALL_COLOUR if c != self.colour]:
                child_states += state.successor_states(other_colour)
            for child in child_states:
                v = min(v, self.brs(child, a, b, depth-1, True))
                b = min(b, v)
                if a > b:
                    break
            return v


    def brs_negamax(self, state, a, b, depth, turn):

        if depth <= 0:
            return eval_state(state, self.colour, self.cost_dict)

        if turn:
            # if it is our turn, find all our moves
            moves = state.get_all_moves(self.colour)
            # set the next turn to NOT our turn
            turn = False
        else:
            # otherwise find all possible opponent moves
            moves = []
            for opponent in [c for c in ALL_COLOUR if c != self.colour]:
                moves += state.get_all_moves(opponent)
            # set the next turn to our turn
            turn = True

        for move in moves:
            current_positions = deepcopy(state.position_dict)

            # apply a move to the current state
            state.make_move(move[0], move[1])
            #
            v = -self.brs_negamax(state, -b, -a, depth - 1, turn)
            # self.unmake_move(move)
            state.position_dict = current_positions
            if v > b:
                return v
            a = max(a, v)

        return a



def eval_state(state: State, colour : str, cost_dict) -> float:
    # the score of the player's position being evaluated
    score = state.score_dict[colour]

    # the number of pieces we have
    num_friendly_pieces = len(state.position_dict[colour])
    hostile_pieces = []
    # build an array of the opponents pieces
    for other_colour in [c for c in ALL_COLOUR if c != colour]:
        hostile_pieces += state.position_dict[other_colour]

    # count the opponents pieces
    num_hostile_pieces = len(hostile_pieces)

    total_dist = 0

    # count the total distance of all our pieces
    for piece in state.position_dict[colour]:

        total_dist += cost_dict[piece]
    # calculate the approximate average distance. Add 1 to divisor for no
    # divide by 0 error.
    avg_dist = total_dist/(1+num_friendly_pieces)

    print(score)
    print(avg_dist)
    print(num_hostile_pieces)

    return -avg_dist + 10*score - num_hostile_pieces



def cubify(pos):
    return (pos[0], pos[1], -pos[0]-pos[1])


def euclidian_distance(action, exit_pos):
    cube_action = cubify(action)
    cube_exit = cubify(exit_pos)
    distance = (cube_action[0] - cube_exit[0])**2 + (cube_action[1] - cube_exit[1])**2 + (cube_action[2] - cube_exit[2])**2
    return distance
