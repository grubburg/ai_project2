from electric_sheep.board import *
from copy import deepcopy
import numpy
import heapq


class State:
    """
    Maintains a representation of the state of the game at a given stage in a format
    suitable to the current Strategy
    Tracks positions of all pieces, scores of all players, and the move
    that was made to arrive at the given state.
    """
    def __init__(self, position_dict, score_dict, arrive_by_move, path_costs, colour_passed):
        self.position_dict = position_dict
        self.score_dict = score_dict
        self.arrived_by_move = arrive_by_move
        self.path_costs = path_costs
        self.colour_passed = colour_passed
        self.value = 0
        self.value = self.simple_eval(colour_passed)

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        state_rep = tuple(sorted([(k, tuple(sorted(v))) for k, v in self.position_dict.items()]))
        return hash(state_rep)

    def simple_eval(self, colour):
        """
        provide a rough estimate of the 
        eval value of the state
        """

        positions = self.position_dict
        distances = [self.path_costs[position] for position in positions[colour]]
        lowest_dists = heapq.nsmallest(4, distances)

        if len(lowest_dists) > 0:
            avg_dist = sum(lowest_dists)/len(lowest_dists)
        else:
            avg_dist = 0

        num_pieces = len(positions[colour])
        score = -avg_dist + (num_pieces + self.score_dict[colour])

        return score + numpy.random.uniform(0.01, 0.02)

    def successor_states(self, colour):
        """
        Method to return all the states that result from a action made by the player 'colour'
        States are returned as an array of states.
        :param colour: the player moving
        :return: array of states that result from those actions
        """
        child_states = []

        actions = self.get_all_actions(colour)

        for action in actions:
            # generate states resulting from exit move
            if action[0] == "EXIT":
                # update position information
                new_position_dict = deepcopy(self.position_dict)
                new_position_dict[colour].remove(action[1])
                # update score information
                new_score_dict = deepcopy(self.score_dict)
                new_score_dict[colour] += 1
                new_state = State(new_position_dict, new_score_dict, action, self.path_costs, self.colour_passed)
                child_states.append(new_state)

            if action[0] == "MOVE":
                # update position information
                new_position_dict = deepcopy(self.position_dict)
                new_position_dict[colour].remove(action[1][0])
                new_position_dict[colour].append(action[1][1])

                new_state = State(new_position_dict, self.score_dict, action, self.path_costs, self.colour_passed)
                child_states.append(new_state)

            if action[0] == "JUMP":
                # update position information
                new_position_dict = deepcopy(self.position_dict)
                middle_piece = tuple(numpy.add(action[1][0], action[1][1]) / 2)
                new_position_dict[colour].remove(action[1][0])
                new_position_dict[colour].append(action[1][1])

                for other_colour in [c for c in ALL_COLOUR if c != colour]:
                    if middle_piece in new_position_dict[other_colour]:
                        new_position_dict[other_colour].remove(middle_piece)
                        new_position_dict[colour].append(middle_piece)
                new_state = State(new_position_dict, self.score_dict, action, self.path_costs, self.colour_passed)
                child_states.append(new_state)

            if action[0] == "PASS":
                child_states.append(self)
        return child_states

    def get_all_actions(self, colour):
        """
        Method to return all action that can be made by a given player.
        :param colour: the player whos actions we are finding
        :return: a list of action that can be made by the player
        """
        valid_actions = []
        if len(self.position_dict[colour]) == 0:
            valid_actions.append(PASS)
            return valid_actions
        for piece in tuple(self.position_dict[colour]):

            # exit action
            if piece in FINISHING_HEXES[colour]:
                new_exit = ("EXIT", piece)
                valid_actions.append(new_exit)

            for move in MOVE_ACTIONS:
                # find new position
                new_pos = tuple(numpy.add(piece, move))

                if new_pos in VALID_TILES:
                    all_pieces = []
                    for c in ALL_COLOUR:
                        all_pieces += self.position_dict[c]

                    # move action
                    if new_pos not in all_pieces:
                        new_move = ("MOVE", (piece, tuple(new_pos)))
                        valid_actions.append(new_move)

                    else:
                        new_pos = tuple(numpy.add(tuple(new_pos), move))
                        if new_pos not in all_pieces and new_pos in VALID_TILES:
                            new_jump = ("JUMP", (piece, tuple(new_pos)))
                            valid_actions.append(new_jump)
                                
        return valid_actions

    def make_action(self, action, colour):

        if action[0] == "JUMP":
            # find jumped over piece
            middle_piece = tuple(numpy.add(action[1][0], action[1][1]) / 2)

            self.position_dict[colour].remove(action[1][0])
            self.position_dict[colour].append(action[1][1])
            if middle_piece not in self.position_dict[colour]:
                for player in [c for c in ALL_COLOUR if c != colour]:
                    if middle_piece in self.position_dict[player]:
                        self.position_dict[player].remove(middle_piece)
                        self.position_dict[colour].append(middle_piece)

        elif action[0] == "MOVE":
            self.position_dict[colour].remove(action[1][0])
            self.position_dict[colour].append(action[1][1])

        elif action[0] == "EXIT":
            self.position_dict[colour].remove(action[1])
            self.score_dict[colour] += 1


class Strategy:

    def __init__(self, state, colour, cost_dict, transpo_table):
        self.state = state
        self.colour = colour
        self.cost_dict = cost_dict
        self.states_checked = 0
        self.transpo_table = transpo_table

    def get_next_move(self):
        """
        Function to return the next move the player should make.
        Employs 'best reply search' defined in brs()
        """
        best_score = -INF
        best_move = PASS

        if len(self.state.position_dict[self.colour]) == 0:
            return best_move

        for child in self.state.successor_states(self.colour):
            if child in self.transpo_table:
                current_score = self.transpo_table[child]

            else:
                current_score = self.brs(child, -INF, INF, 2, False)
                self.transpo_table[child] = current_score

            # current_score = self.brs(child, -INF, INF, 3, False)
            if current_score > best_score:
                best_score = current_score
                best_move = child.arrived_by_move

        # convert to JSON serializable format
        if best_move[0] == "EXIT":
            return best_move[0], (int(best_move[1][0]), int(best_move[1][1]))

        else:
            return best_move[0], ((int(best_move[1][0][0]), int(best_move[1][0][1])),
                                  (int(best_move[1][1][0]), int(best_move[1][1][1])))

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
            self.states_checked += 1
            return eval_state(state, self.colour, self.cost_dict)
        # if it is the root players turn
        if turn:
            # initialise the value to negative infinity
            v = -INF
            # find all states emanating from root player's actions
            for child in sorted(state.successor_states(self.colour), reverse=True)[:4]:

                if child in self.transpo_table:
                    v = self.transpo_table[child]

                else:
                    v = max(v, self.brs(child, a, b, depth-1, False))
                    self.transpo_table[child] = v

                a = max(a, v)
                if a >= b:
                    break
            return v

        # let both enemies have their turn
        else:
            v = INF
            child_states = []
            for other_colour in [c for c in ALL_COLOUR if c != self.colour]:
                child_states += state.successor_states(other_colour)
            for child in sorted(child_states, reverse=True):
                if child in self.transpo_table:
                    v = self.transpo_table[child]

                else:
                    v = min(v, self.brs(child, a, b, depth-1, True))
                    self.transpo_table[child] = v

                b = min(b, v)
                if a >= b:
                    break
            return v


def eval_state(state: State, colour : str, cost_dict) -> float:

    # the score of the player's position being evaluated
    score = state.score_dict[colour]

    # have reached win condition
    if score >= 4:
        return 10000
    
    # the number of pieces we have
    num_friendly_pieces = len(state.position_dict[colour])
    hostile_pieces = []
    # build an array of the opponents pieces
    for other_colour in [c for c in ALL_COLOUR if c != colour]:
        hostile_pieces += state.position_dict[other_colour]

    # count the opponents pieces
    num_hostile_pieces = len(hostile_pieces)

    total_dist = 0
    avg_dist = state.value

    return avg_dist + score - num_hostile_pieces + numpy.random.uniform(0.01, 0.02)
