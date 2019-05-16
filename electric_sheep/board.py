from electric_sheep.hexagon import *
import heapq


RED_START = ((-3,3), (-3,2), (-3,1), (-3,0))
GREEN_START = ((0,-3), (1,-3), (2,-3), (3,-3))
BLUE_START = ((3, 0), (2, 1), (1, 2), (0, 3))




class Board:
    # ================== Constants ================================== #
    BLOCK = "blk"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

    MOVE_ACTIONS = [[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]]

    # exit position for each player
    FINAL_ROWS = {RED: [[3, -3], [3, -2], [3, -1], [3, 0]],
                  GREEN: [[-3, 3], [-2, 3], [-1, 3], [0, 3]],
                  BLUE: [[-3, 0], [-2, -1], [-1, -2], [0, -3]]}

    # =============================================================== #
    def __init__(self, colour):
        self.hexagon_dict = {}
        self.position_dict = {}
        self.create_hexagons()
        self.create_positions()
        self.score = 0
        self.colour = colour
        self.printable_board = self.create_printable_board()
        self.path_costs = self.shortest_path_costs(self.colour)

    def create_hexagons(self):
        ran = range(-3, +3+1)
        for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
            if qr in RED_START:
                my_hex = Hexagon(qr, "red")
            elif qr in GREEN_START:
                my_hex = Hexagon(qr, "green")
            elif qr in BLUE_START:
                my_hex = Hexagon(qr, "blue")
            else:
                my_hex = Hexagon(qr, "e")
    
            self.hexagon_dict[tuple(qr)] = my_hex
    
    # create a dictionary of positions for each colour
    def create_positions(self):
        red = list(RED_START)
        green = list(GREEN_START)
        blue = list(BLUE_START)

        self.position_dict['red'] = red
        self.position_dict['green'] = green
        self.position_dict['blue'] = blue



    def is_valid_position(self, positon):
        if tuple(positon) in self.hexagon_dict:
            return True
        else:
            return False

    def create_printable_board(self):
        """
        creates the map of the board
        add each legal position of the board into a dictionary
        """
        out_board = {}
        ran = range(-3, +3 + 1)

        for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
            out_board[qr] = ""

        return out_board

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
        for tile in self.FINAL_ROWS[colour]:

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

        for move in self.MOVE_ACTIONS:
            new_tile = [a + b for a, b in zip(tile, move)]
            all_tiles.append(new_tile)

        return [x for x in all_tiles if tuple(x) in self.printable_board]