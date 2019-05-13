from electric_sheep.hexagon import *
from electric_sheep.board import *
from electric_sheep.randomStrat import Strategy
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
        self.strategy = Strategy()


    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        next_action = self.strategy.get_next_move(self)
        return next_action


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        if action[0] == "JUMP":
            #find jumped over piece
            middle_piece = tuple(numpy.add(action[1][0], action[1][1]) / 2)

            #if capturing piece
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
    
    def exit_piece(self, positon):
        if positon in self.pieces:
            self.pieces.remove(positon)
