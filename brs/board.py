from brs.hexagon import *



RED_START = ((-3,3), (-3,2), (-3,1), (-3,0))
GREEN_START = ((0,-3), (1,-3), (2,-3), (3,-3))
BLUE_START = ((3, 0), (2, 1), (1, 2), (0, 3))



class Board:
    def __init__(self):
        self.hexagon_dict = {}
        self.position_dict = {}
        self.create_hexagons()
        self.create_positions()
        self.score = 0


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
