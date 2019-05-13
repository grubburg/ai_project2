from electric_sheep.hexagon import *
from electric_sheep.board import *
from electric_sheep.brsStrat import Strategy
import numpy


class Player:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        self.colour = colour
        self.board = Board()
        self.pieces = self.assign_pieces()



    def action(self):

        # create a strategy object based on the current layout of the board
        # this
        strategy = Strategy(self.board)

        # retrieve the next action based on the current state
        next_action = self.strategy.get_next_move(self, state)
        return next_action

    def update(self, colour, action):

        if action[0] == "JUMP":
            # find jumped over piece
            middle_piece = tuple(numpy.add(action[1][0], action[1][1]) / 2)

            # if capturing piece
            if self.board.hexagon_dict[middle_piece].occupant != colour:
                if self.colour == colour:
                    self.pieces.append(middle_piece)
                elif self.board.hexagon_dict[middle_piece].occupant == self.colour:
                    self.pieces.remove(middle_piece)

                self.board.hexagon_dict[middle_piece].occupant = colour

            self.board.hexagon_dict[action[1][0]].occupant = "e"
            self.board.hexagon_dict[action[1][1]].occupant = colour
            self.move_pieces(action[1])
        elif action[0] == "MOVE":

            self.board.hexagon_dict[action[1][0]].occupant = "e"
            self.board.hexagon_dict[action[1][1]].occupant = colour
            self.move_pieces(action[1])
        elif action[0] == "EXIT":
            self.board.hexagon_dict[action[1]].occupant = "e"
            self.exit_piece(action[1])

    def assign_pieces(self):
        if self.colour == "red":
            return list(RED_START)
        elif self.colour == "green":
            return list(GREEN_START)
        else:
            return list(BLUE_START)

    def move_pieces(self, action):
        if action[0] in self.pieces:
            self.pieces.remove(action[0])
            self.pieces.append(action[1])

    def exit_piece(self, position):
        if position in self.pieces:
            self.pieces.remove(position)
