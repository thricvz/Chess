import pygame as pg
import string

#Board Class
class Board():
    
    def __init__(self,dimensions = (512,512)):
        self.SCREEN = pg.display.set_mode(dimensions)                                                                          #creates a 400 by 400 window
        self.TILE_SIZE = dimensions[0] // 8
        self.BRIGHT_TILE = pg.transform.scale(pg.image.load("Assets\\square brown light_png_128px.png") , (self.TILE_SIZE,self.TILE_SIZE))
        self.DARK_TILE = pg.transform.scale(pg.image.load("Assets\\square brown dark_png_128px.png") , (self.TILE_SIZE,self.TILE_SIZE))        
        self.DOT = pg.transform.scale(pg.image.load("Assets\\dot.png"), (64, 64))
        self.DOT_SIZE = self.DOT.get_width()                             #loads the dark and light square sprites
        self.FONT = pg.font.SysFont(None, 20)

        

        self.board_state = {'a8': None, 'b8': None, 'c8': None, 'd8': None, 'e8': None, 'f8': None, 'g8': None, 'h8': None,
                            'a7': None, 'b7': None, 'c7': None, 'd7': None, 'e7': None, 'f7': None, 'g7': None, 'h7': None,
                            'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
                            'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
                            'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
                            'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
                            'a2': None, 'b2': None, 'c2': None, 'd2': None, 'e2': None, 'f2': None, 'g2': None, 'h2': None,
                            'a1': None, 'b1': None, 'c1': None, 'd1': None, 'e1': None, 'f1': None, 'g1': None, 'h1': None}
        
        self.board_pos = list(self.board_state)            #list that serves as indicator for the pieces 

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
            case_index = self.board_pos.index(case)                 #gets the index of the element
            board_ocupation = self.board_state[case]                #gets what is in the case

            row = case_index // 8                                   #gets its supposed row and its supposed row
            column = case_index % 8                                 #ex : case a1 -> 56 in list -> row: 7 column : 0 (count started from 0)
            #case text
            text = self.FONT.render(case, True, (255,255,255))


            if board_ocupation != None: 
                self.SCREEN.blit(board_ocupation.sprite,(column * self.TILE_SIZE + board_ocupation.adjustment,row * self.TILE_SIZE))   #draws the content if it is existent ###need t add adjustement system
            self.SCREEN.blit(text,(column * self.TILE_SIZE + (self.TILE_SIZE * 0.75),row * self.TILE_SIZE + (self.TILE_SIZE * 0.8)))            ###not adjustable need to fix this


    def get_clicked_case(self,event_list):
        if event_list.type == pg.MOUSEBUTTONUP:                         #if mouse is pressed then:
            mouse_x,mouse_y = pg.mouse.get_pos()                        #gets the mouse coordinates
            case_column = (mouse_x // self.TILE_SIZE)                   #transforms it into the corresponding row and column (count starts at 1)
            case_row = (mouse_y // self.TILE_SIZE) 
            self.selected_case = self.board_pos[case_row * 8 + case_column]

        return self
        
    def move():
        pass

    def predict():
        pass



class Piece():
    mouvement_axis_map = {"pawn": 8 ,"rook" : [1,8],"knight" : [10,14,15,16,17],"bishop" : [7,9] ,"queen" : [1,7,8,9],"king" : [1,7,8,9]}

    def __init__(self,type,color):
        self.color = color
        self.type = type
        self.sprite = pg.transform.scale(pg.image.load(f"Assets\\{self.color[0]}_{self.type}_png_128px.png"),(60,60))
        self.mouvement_axis = Piece.mouvement_axis_map[self.type]
        self.times_moved = 0
        self.adjustment = 0


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
