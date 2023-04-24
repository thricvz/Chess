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
        self.already_selected = False
        self.dotted_cases = []

    def coords(self,case):
        case_index = self.board_pos.index(case)  
        return case_index % 8,case_index // 8

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

        ###to redo 
        for case in self.board_pos:
            board_ocupation = self.board_state[case]                #gets what is in the case
            case_x,case_y = self.coords(case)                                 #ex : case a1 -> 56 in list -> row: 7 column : 0 (count started from 0)
            
            text = self.FONT.render(case, True, (255,255,255))             #case text

            if board_ocupation != None: 
                self.SCREEN.blit(board_ocupation.sprite,(case_x * self.TILE_SIZE,case_y * self.TILE_SIZE))   #draws the content if it is existent ###need t add adjustement system
                if board_ocupation.clicked and self.dotted_cases != None:
                    for dot in self.dotted_cases:
                        dot_x,dot_y = self.coords(dot)
                        self.SCREEN.blit(self.DOT,((dot_x - 1) * self.TILE_SIZE + self.TILE_SIZE ,(dot_y - 1) * self.TILE_SIZE + self.TILE_SIZE))

            self.SCREEN.blit(text,(case_x * self.TILE_SIZE ,case_y * self.TILE_SIZE))

    def clicked(self):
        if pg.mouse.get_pressed()[0]:   #if mouse is pressed then:
                mouse_x,mouse_y = pg.mouse.get_pos()    #gets the mouse coordinates
                case_column = (mouse_x // self.TILE_SIZE)   #transforms it into the corresponding row and column (count starts at 1)
                case_row = (mouse_y // self.TILE_SIZE)

                pg.time.delay(200) #delay that prevents the dot from blinking fast

                clicked_case = self.board_pos[case_row * 8 + case_column]
                self.clicked_piece = self.board_state[clicked_case]

                if not self.already_selected:
                    self.selected_case = clicked_case   #updating piece status and board attribute
                    self.clicked_piece.clicked = True
                    self.already_selected = True
                    self.dotted_cases = self.predict()


                elif clicked_case == self.selected_case and self.already_selected:
                    self.clicked_piece.clicked = False
                    self.already_selected = False
                    self.clicked_piece = None
                    self.dotted_cases = []
                return True

        return False
    def move(self):
        pass
    def predict(self):  #too much if else statements need to find a more algoritmic way to solve this problem
        axes = self.clicked_piece.mouvement_axis
        x = self.board_pos.index(self.selected_case)
        mouv_type = self.clicked_piece.mouvement_type
        predicted_positions = []

        for axis in axes:
            if mouv_type == "continous":
                N = 1
                generated_index = x + N * axis

                while generated_index in range(len(self.board_pos)):
                    generated_position =  self.board_pos[generated_index]
                    #conditions of movement
                    if self.board_state[generated_position] == None:
                        predicted_positions.append(generated_index)
                    elif self.board_state[generated_position].color == self.clicked_piece.color:
                        break
                    elif self.board_state[generated_position] != self.clicked_piece.color:
                        predicted_positions.append(generated_index)
                        break
                    elif N == 8:
                        break
                    N += 1
            else:
                pos = self.board_pos[x + axis]
                predicted_positions.append(pos)
        #now for uncontinous pieces
        return predicted_positions
        pass 

class Piece():
    mouvement_axis_map = {"pawn": [8] ,"rook" : [1,8],"knight" : [6,-6,10,-10,-15,15,17,-17],"bishop" : [7,9] ,"queen" : [1,7,8,9],"king" : [1,7,8,9]}
    def __init__(self,type,color):
        self.color = color
        self.type = type
        self.sprite = pg.transform.scale(pg.image.load(f"Assets\\{self.color[0]}_{self.type}_png_128px.png"),(64,64))
        self.mouvement_axis = Piece.mouvement_axis_map[self.type]
        self.mouvement_type = "discontinous" if self.type  in ["king","knight","pawn"] else "continous"
        self.times_moved = 0
        self.clicked = False


    """def predict(self):
        current_pos_index  = Board.board_pos.index(self.current_pos)         #gets the numerical value of current position
        self.possible_moves = []

        ###Iturn code cleaner & the 2 case mouvement from start

        if Board.board_state[Board.board_pos[current_pos_index -  self.mouvement_axis]] == None :             #if the case before him is empty
            self.possible_moves.append(Board.board_pos[current_pos_index -  self.mouvement_axis])
        
        if Board.board_pos[current_pos_index] in Board.board_right_border:           #if pawn on right border
            if Board.board_state[Board.board_pos[current_pos_index - 9]] != None and Board.board_state[self.board_pos[current_pos_index - 9]].color != self.color:        #if left diagonal not empty
                self.possible_moves.append(self.board_pos[current_pos_index - 9])                                                                                                             

        elif Board.board_pos[current_pos_index] in Board.board_left_border:
             if Board.board_state[Board.board_pos[current_pos_index - 7]] != None and Board.board_state[Board.board_pos[current_pos_index - 7]].color != self.color:        #if right diagonal not empty
                self.possible_moves.append(Board.board_pos[current_pos_index - 7])                   

        else:
            if Board.board_state[Board.board_pos[current_pos_index - 9]] != None and Board.board_state[Board.board_pos[current_pos_index - 9]].color != self.color:        #if left diagonal not empty
                self.possible_moves.append(Board.board_pos[current_pos_index - 9])

            elif Board.board_state[self.board_pos[current_pos_index - 7]] != None and Board.board_state[Board.board_pos[current_pos_index - 7]].color != self.color:        #if right diagonal not empty
                self.possible_moves.append(Board.board_pos[current_pos_index - 7])   

        ###displaying the dots
        self.possible_moves_indexes = [Board.board_pos.index(coord) for coord in self.possible_moves]
        for index in self.possible_moves_indexes:
            row = index // 8                                   
            column = index % 8  
            Board.SCREEN.blit(self.dot,(column * 128 + self.dot_size / 2,row * 128 + self.dot_size / 2))

    ####second to complete
    def place(self):
        Board.board_state[self.board_pos[self.board_pos.index(self.current_pos)]] = self

    def move(self,pos):      ### need to implement the idea of acessing the pos with mouse click
        #self.predict()
        #if pos in self.possible_moves:
        Board.board_state[pos] = self #puts the element in its future position by using slicing 
        Board.board_state[Board.board_pos[Board.board_pos.index(self.current_pos)]] = None                        #replaces the precedent position with a void
        self.current_pos = pos"""


########to do other pieces
