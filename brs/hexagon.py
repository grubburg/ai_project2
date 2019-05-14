import numpy

MOVE_ACTIONS = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]

class Hexagon:
    def __init__(self, position, occupant):
        self.positon = tuple(position)
        self.occupant = occupant
        self.neighbours = self.create_neightbours()


    def create_neightbours(self):
        neighbour_list = []
        for move in MOVE_ACTIONS:
            new_tile = numpy.add(self.positon, move)
            if is_valid_position(new_tile):
                neighbour_list.append(tuple(new_tile))
        return neighbour_list

def is_valid_position(positon) ->bool:
    ran = range(-3, +3 + 1)
    if -positon[0] -positon[1] in ran:
        return True
    else:
        return False


