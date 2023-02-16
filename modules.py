import pygame as pg
import string

#Board Class
class Board():
    #all attributes the pieces need

    board_state = {'a8': None, 'b8': None, 'c8': None, 'd8': None, 'e8': None, 'f8': None, 'g8': None, 'h8': None,
                            'a7': None, 'b7': None, 'c7': None, 'd7': None, 'e7': None, 'f7': None, 'g7': None, 'h7': None,
                            'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
                            'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
                            'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
                            'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
                            'a2': None, 'b2': None, 'c2': None, 'd2': None, 'e2': None, 'f2': None, 'g2': None, 'h2': None,
                            'a1': None, 'b1': None, 'c1': None, 'd1': None, 'e1': None, 'f1': None, 'g1': None, 'h1': None}
    board_pos = list(board_state)            #list that serves as indicator for the pieces 

    board_top_border = ['a8','b8','c8','d8','e8','f8','g8','h8'] 
    board_right_border = ['h7','h6','h5','h4','h3','h2','h1']
    board_bottom_border = ['h1','g1','f1','e1','d1','c1','b1','a1']
    board_left_border = ['a1','a2','a3','a4','a5','a6','a7']


    def __init__(self):
        self.screen = pg.display.set_mode((1024,1024))                                                                          #creates a 400 by 400 window
        self.dark_tile = pg.image.load("/home/eric/Documents/Coding projects/Chess/Assets/square brown dark_png_128px.png")     #loads the dark and light square sprites
        self.bright_tile = pg.image.load("/home/eric/Documents/Coding projects/Chess/Assets/square brown light_png_128px.png")

    def generate_pieces(self):
        self.pieces_coordinates_on_board = {"white" : 
                {
                    "pawn" : ["a7","b7","c7","d7","e7","f7","h7","g7"],
                },
                "black" : {
                    "pawn" : ["a2","b2","c2","d2","e2","f2","h2","g2"]
                }
            }
        for player_color in self.pieces_coordinates_on_board:
            for piece_name in self.pieces_coordinates_on_board[player_color]: 
                piece_positions = self.pieces_coordinates_on_board[player_color][piece_name]
                for position in piece_positions:
                    if piece_name == "pawn":
                        current_piece = Pawn(player_color,position)
                        current_piece.place()

    def build(self):
        tiles = [self.dark_tile,self.bright_tile]
        tiles_side_length = tiles[0].get_size()[0]        #gets the length/heigth value of the square(value equal to both)
        
        for row_number in range(0,9):                #loop that gets the order number in the x axis
            for column_number in range(0,9):             #loop that gets the order number in the y axis
                current_tile = tiles[0]                  #changes the square on every iteration to create the pattern
                tiles.reverse()

                self.screen.blit(current_tile,(row_number * tiles_side_length,column_number * tiles_side_length))    #draws the tile

        ###to redo 
        for case in self.board_pos:
            case_index = self.board_pos.index(case)                 #gets the index of the element
            board_ocupation = self.board_state[case]                #gets what is in the case

            row = case_index // 8                                   #gets its supposed row and its supposed row
            column = case_index % 8                                 #ex : case a1 -> 56 in list -> row: 7 column : 0 (count dtarted from 0)

            if board_ocupation != None:
                self.screen.blit(board_ocupation.sprite,(column * tiles_side_length + board_ocupation.adjustment,row * tiles_side_length))   #draws the content if it is existent ###need t add adjustement system
                

class Pawn(Board):
    def __init__(self,color,initial_pos):
        self.color = color              #specifies the color of the piece **must be a string**
        self.sprite = pg.image.load("/home/eric/Documents/Coding projects/Chess/Assets/"+ self.color[0] +"_pawn_png_128px.png")
        self.adjustment = 11                #little amount of space to adjust the image only for pawn

        self.current_pos = initial_pos  #sets current position to the initial 
        self.mouvement_axis = 8        #pawn can go one square forward at the time **here it corresponds to 10 in the board_ps list**
        self.times_moved = 0            #tracks the amount of time piece was moved
                
        

        self.dot = pg.image.load("/home/eric/Documents/Coding projects/Chess/Assets/dot.png")
        self.dot = pg.transform.scale(self.dot, (64, 64))
        self.dot_size = self.dot.get_width()

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
            Board.screen.blit(self.dot,(column * 128 + self.dot_size / 2,row * 128 + self.dot_size / 2))
"""
    ####second to complete
    def place(self):
        Board.board_state[self.board_pos[self.board_pos.index(self.current_pos)]] = self

    def move(self,pos):      ### need to implement the idea of acessing the pos with mouse click
        #self.predict()
        #if pos in self.possible_moves:
        Board.board_state[pos] = self #puts the element in its future position by using slicing 
        Board.board_state[Board.board_pos[Board.board_pos.index(self.current_pos)]] = None                        #replaces the precedent position with a void
        self.current_pos = pos


########to do other pieces
