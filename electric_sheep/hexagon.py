from electric_sheep.data import MOVE_ACTIONS, is_valid_position
import numpy

class Hexagon:
    def __init__(self, position, occupant):
        self.positon = tuple(position)
        self.occupant = occupant
        self.neighbours = self.create_neighbours()

    def create_neighbours(self):
        neighbour_list = []
        for move in MOVE_ACTIONS:
            new_tile = numpy.add(self.positon, move)
            if is_valid_position(new_tile):
                neighbour_list.append(tuple(new_tile))
        return neighbour_list

