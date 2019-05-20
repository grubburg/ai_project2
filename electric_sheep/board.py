from electric_sheep.hexagon import *
from electric_sheep.data import *
import heapq



class Board:
    """
    Default board representation of the current game
    hexgon dict holds a representation of the whole board
    position dict holds location of pieces for each colour
    score_dict counts the number of pieces exited by each colour
    path_cost stores the number of moves required to reach exit 
    for specified colour

    """
    def __init__(self, colour):
        self.hexagon_dict = {}
        self.position_dict = {}
        self.score_dict = {}
        self.create_hexagons()
        self.create_positions()
        self.create_scores()

        self.path_costs = self.shortest_path_costs(colour)


    def create_hexagons(self):
        """
        Fills up the hexagon dict with the starting state 
        of the game
        """
        for qr in VALID_TILES:
            if qr in RED_START:
                my_hex = Hexagon(qr, 'red')
            elif qr in GREEN_START:
                my_hex = Hexagon(qr, 'green')
            elif qr in BLUE_START:
                my_hex = Hexagon(qr, 'blue')
            else:
                my_hex = Hexagon(qr, EMPTY)
    
            self.hexagon_dict[tuple(qr)] = my_hex
    
    # create a dictionary of positions for each colour
    def create_positions(self):
        """
        initializes the positon dict with the starting
        positons of the game
        """
        red = list(RED_START)
        green = list(GREEN_START)
        blue = list(BLUE_START)

        self.position_dict['red'] = red
        self.position_dict['green'] = green
        self.position_dict['blue'] = blue

    def create_scores(self):
        self.score_dict['red'] = 0
        self.score_dict['green'] = 0
        self.score_dict['blue'] = 0

    def shortest_path_costs(self, colour):
        """
        uses dijkstra's to find the shortest path from the any final row to all other positions
        and returns a dictionary with all the costs
        """
        # assume all final_row pieces can access exit position
        cost_dict = {}
        entry_point = 0
        queue = []

        # add all final pieces to queue with cost 1
        for tile in FINISHING_HEXES[colour]:

            # a 3 point vector added to resolve same cost position sorting in heap
            queue.append([1, entry_point, tuple(tile)])
            cost_dict[tuple(tile)] = 1
            entry_point += 1
        heapq.heapify(queue)

        # while not visited tiles exist
        while queue:
            curr_tile = heapq.heappop(queue)

            # find cost for all adjacent tiles
            for adjacent_tile in self.find_adjacent_tiles(curr_tile[2]):

                # if adjacent tile not seen before
                if tuple(adjacent_tile) not in cost_dict:
                    cost_dict[tuple(adjacent_tile)] = curr_tile[0] + 1
                    heapq.heappush(queue, [curr_tile[0] + 1, entry_point, tuple(adjacent_tile)])
                    entry_point += 1

                # adjust if this path to adjacent tile is shorter
                elif cost_dict[tuple(adjacent_tile)] > curr_tile[0] + 1:
                    cost_dict[tuple(adjacent_tile)] = curr_tile[0] + 1

        return cost_dict

    def find_adjacent_tiles(self, tile):
        """
        Returns all the possible moves from current tile
        only considers jumps over blocks and not pieces
        """

        all_tiles = []

        for move in MOVE_ACTIONS:
            new_tile = [a + b for a, b in zip(tile, move)]
            all_tiles.append(new_tile)

        return [x for x in all_tiles if tuple(x) in VALID_TILES]