import pygame as pg
import string

#Board Class
class Board():
    
    def __init__(self,dimensions = (512,512)):
        self.SCREEN = pg.display.set_mode(dimensions)   #creates a 400 by 400 window
        self.TILE_SIZE = dimensions[0] // 8
        self.BRIGHT_TILE = pg.transform.scale(pg.image.load("Assets\\square brown light_png_128px.png") , (self.TILE_SIZE,self.TILE_SIZE))
        self.DARK_TILE = pg.transform.scale(pg.image.load("Assets\\square brown dark_png_128px.png") , (self.TILE_SIZE,self.TILE_SIZE))        
        self.DOT = pg.transform.scale(pg.image.load("Assets\\dot.png"), (64, 64))
        self.DOT_SIZE = self.DOT.get_width()    #loads the dark and light square sprites
        self.FONT = pg.font.SysFont(None,20)

        

        self.board_state = {'a8': None, 'b8': None, 'c8': None, 'd8': None, 'e8': None, 'f8': None, 'g8': None, 'h8': None,
                            'a7': None, 'b7': None, 'c7': None, 'd7': None, 'e7': None, 'f7': None, 'g7': None, 'h7': None,
                            'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
                            'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
                            'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
                            'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
                            'a2': None, 'b2': None, 'c2': None, 'd2': None, 'e2': None, 'f2': None, 'g2': None, 'h2': None,
                            'a1': None, 'b1': None, 'c1': None, 'd1': None, 'e1': None, 'f1': None, 'g1': None, 'h1': None}
        
        self.board_pos = list(self.board_state)     #list that serves as indicator for the pieces
        self.board_pos = [self.board_pos[x:x+8] for x in range(0, len(self.board_pos), 8)]
        self.piece_already_selected = False               #responsible for seeeing if a piece is selected
        self.dotted_cases = []

    def coords(self,case):
        x = int(ord(case[0])-97)
        y = abs(int(case[1]) - 8)
        return x,y

    def generate_pieces(self):
        piece_positions = {
            "pawn" : ["a7","b7","c7","d7","e7","f7","g7","h7","a2","b2","c2","d2","e2","f2","g2","h2",] ,
            "rook" : ["a8","h8","a1","h1"],
            "knight"  : ["b8","g8","b1","g1"],
            "bishop" : ["c8","f8","c1","f1"],
            "queen" : ["d8","d1"],
            "king"  : ["e8","e1"],
        }

        for piece in piece_positions.items():
            color = "black"
            for position in piece[1]:
                if piece[1].index(position) == len(piece[1]) / 2 : color = "white"
                self.board_state[position] = Piece(piece[0],color)
     

    def build(self):
        tiles = [self.DARK_TILE,self.BRIGHT_TILE]
        for row_number in range(0,9):                #loop that gets the order number in the x axis
            for column_number in range(0,9):             #loop that gets the order number in the y axis
                current_tile = tiles[0]                  #changes the square on every iteration to create the pattern
                tiles.reverse()

                self.SCREEN.blit(current_tile,(row_number * self.TILE_SIZE,column_number * self.TILE_SIZE))    #draws the tile

        for dot in self.dotted_cases:
            dot_x, dot_y = self.coords(dot)
            self.SCREEN.blit(self.DOT, ((dot_x - 1) * self.TILE_SIZE + self.TILE_SIZE, (dot_y - 1) * self.TILE_SIZE + self.TILE_SIZE))

        for row in self.board_pos:
            for case in row:
                board_ocupation = self.board_state[case]                #gets what is in the case
                case_x,case_y = self.coords(case)                                 #ex : case a1 -> 56 in list -> row: 7 column : 0 (count started from 0)

                text = self.FONT.render(case, True, (255,255,255))             #case text

                if board_ocupation != None:
                    self.SCREEN.blit(board_ocupation.sprite, (case_x * self.TILE_SIZE,case_y * self.TILE_SIZE))  # displays the piece itself

                self.SCREEN.blit(text,(case_x * self.TILE_SIZE ,case_y * self.TILE_SIZE))

    def manage_click(self):
        if pg.mouse.get_pressed()[0]:   #if mouse is pressed then:
                mouse_x,mouse_y = pg.mouse.get_pos()    #gets the mouse coordinates
                case_column = (mouse_x // self.TILE_SIZE)   #transforms it into the corresponding row and column (count starts at 1)
                case_row = (mouse_y // self.TILE_SIZE)

                pg.time.delay(200) #delay that prevents the dot from blinking fast

                current_clicked_case = self.board_pos[case_row][case_column]

                if not self.piece_already_selected:
                    if self.board_state[current_clicked_case] != None:
                        self.selected_board_case  = current_clicked_case
                        self.piece_already_selected = True
                        self.dotted_cases = self.predict(self.selected_board_case)


                else:
                    if current_clicked_case == self.selected_board_case or current_clicked_case in self.dotted_cases:
                        self.move(current_clicked_case)

                        self.piece_already_selected = False
                        self.dotted_cases = []
        return self
    def move(self,new_case):
        self.board_state[new_case] = None
        self.board_state[new_case] = self.board_state[self.selected_board_case]
        self.board_state[self.selected_board_case] = None


    def predict(self,piece_case):  #too much if else statements need to find a more algoritmic way to solve this problem
        predicted_positions = list()
        piece = self.board_state[piece_case]
        piece_position = self.coords(piece_case)


        for step in piece.mouvement_axis:
            for n in range(1, 8): #since the maximum of cases in any direction is 8

                if piece.mouvement_type == "discontinous": n = 1

                if piece_position[0] + n * step[0] in range(8) and piece_position[1] + n * step[1] in range(8):             #checks if the future position  is on the board
                    gen_x = piece_position[0] + n * step[0]
                    gen_y = piece_position[1] + n * step[1]

                    generated_position = self.board_pos[gen_y][gen_x]

                    if self.board_state[generated_position] == None:
                        predicted_positions.append(generated_position)

                    elif self.board_state[generated_position].color != piece.color:
                        predicted_positions.append(generated_position)
                        break

                    elif self.board_state[generated_position].color == piece.color:
                        break
                else:
                    break

        return predicted_positions


class Piece():
    mouvement_axis_map = {
                    "pawn": [(0,-1)] ,"rook" : [(1,0),(0,-1),(-1,0),(0,1)],
                    "knight" : [(-2,1),(-1,2),(-2,-1),(-1,-2),(2,1),(1,2),(2,-1),(1,-2)],
                    "bishop" : [(-1,1),(-1,-1),(1,1),(1,-1)] ,
                    "queen" : [(1,0),(0,-1),(-1,0),(0,1),(-1,1),(-1,-1),(1,1),(1,-1)],
                    "king" : [(1,0),(0,-1),(-1,0),(0,1),(-1,1),(-1,-1),(1,1),(1,-1)]
                          }
    ###this format consists of the "steps" that have to be done on the board (x,y) : ex-> (-1,1) would be one "step" to the left and one "step" to the bottom
    def __init__(self,type,color):
        self.color = color
        self.type = type
        self.sprite = pg.transform.scale(pg.image.load(f"Assets\\{self.color[0]}_{self.type}_png_128px.png"),(64,64))
        self.mouvement_axis = Piece.mouvement_axis_map[self.type]
        self.mouvement_type = "discontinous" if self.type  in ["king","knight","pawn"] else "continous"
        self.times_moved = 0
        self.clicked = False