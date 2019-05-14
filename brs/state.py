from brs.board import *

FINISHING_HEXES = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}


class State:

    def __init__(self):

        self.board = Board()








    def all_valid_actions(self, player):
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

    def eval(self, player):
        return 0

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

