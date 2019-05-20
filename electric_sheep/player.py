from electric_sheep.board import *
from electric_sheep.brsStrat import Strategy as brsStrat, State
from electric_sheep.data import *
import numpy


class Player:
    """
    COMP30024 project 2 sem 1 2019 player
    Written by team electric_sheep
    Asil Mian and John Stephenson
    """
    def __init__(self, colour):
        """
        Initialize player
        """
        self.colour = colour
        self.board = Board(colour)




    def action(self):
        """
        get best next move according to the strategy
        """
        # create a state object based on the current layout of the board
        current_state = State(self.board.position_dict, self.board.score_dict, None, self.board.path_costs, self.colour)

        strat = brsStrat(current_state, self.colour, self.board.path_costs, self.board.transpo_table)
        
        # retrieve the next action based on the current state
        next_action = strat.get_next_move()
        
        return next_action

    def update(self, colour, action):
        """
        updates the internal player board with 
        the moves from referee
        """

        #jump action update
        if action[0] == "JUMP":

            #find jumped over piece
            middle_piece = tuple(numpy.add(action[1][0], action[1][1]) // 2)

            #if a piece was captured
            if self.board.hexagon_dict[middle_piece].occupant != colour:
                cap_colour = self.board.hexagon_dict[middle_piece].occupant
                self.board.position_dict[cap_colour].remove(middle_piece)
                self.board.position_dict[colour].append(middle_piece)
                
                self.board.hexagon_dict[middle_piece].occupant = colour

            self.move_pieces(action, colour)

        elif action[0] == "MOVE":
            self.move_pieces(action, colour)

        elif action[0] == "EXIT":
            self.exit_piece(action, colour)



    def move_pieces(self, action, colour):
        """
        updates the board dictionary and positon list
        """
        self.board.hexagon_dict[action[1][0]].occupant = EMPTY
        self.board.hexagon_dict[action[1][1]].occupant = colour

        self.board.position_dict[colour].remove(action[1][0])
        self.board.position_dict[colour].append(action[1][1]) 

    def exit_piece(self, action, colour):
        """
        updates the board dictionary and positon list
        with exit move
        """
        self.board.hexagon_dict[action[1]].occupant = EMPTY
        self.board.score_dict[colour] += 1
        self.board.position_dict[colour].remove(action[1])
