import pygame 

class Piece(pygame.sprite.Sprite):
    movement_axis_map = {
                    "pawn": [[0,-1]],
                    "rook" : [[1,0],[0,-1],[-1,0],[0,1]],
                    "knight" : [[-2,1],[-1,2],[-2,-1],[-1,-2],[2,1],[1,2],[2,-1],[1,-2]],
                    "bishop" : [[-1,1],[-1,-1],[1,1],[1,-1]] ,
                    "queen" : [[1,0],[0,-1],[-1,0],[0,1],[-1,1],[-1,-1],[1,1],[1,-1]],
                    "king" : [[1,0],[0,-1],[-1,0],[0,1],[-1,1],[-1,-1],[1,1],[1,-1]]
                          }
    ###this format consists of the "steps" that have to be done on the board (x,y) : ex-> (-1,1) would be one "step" to the left and one "step" to the bottom
    def __init__(self,type,color,position):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.color = color
        self.position = position
        self.movement_direction = Piece.movement_axis_map[self.type]
        self.movement_type = "discontinous" if self.type  in ["king","knight","pawn"] else "continous"
        self.possible_moves  = []
        self.attacked_by = []
        self.attacking = []
        self.protected_by = []
        self.protecting = []
        self.exeption = False
        self.times_moved = 0
        #self.image = pygame.transform.scale(pygame.image.load(f"Assets\\{self.color[0]}_{self.type}_png_128px.png"), (64, 64))
        #self.rect = self.image.get_rect()

#Board Class
class Board(Piece):
    
    def __init__(self):
        self.POSITIONS = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.players = ["white","black"]
        self.pieces_in_play = []
        self.turn = self.players[0]

    def build_from_text(self,board_in_text_format):
        #first it divides these positions to ranks (to make the processing easier)
        board_in_text_format =  ''.join(board_in_text_format.splitlines())
        ranks = [board_in_text_format[start_index:start_index+15] for start_index in range(0,len(board_in_text_format),15)]
        piece_symbols = {"k":"king","q":"queen","r":"rook","b":"bishop","n":"knight","p":"pawn"}

        for square_rank,rank in enumerate(ranks):
            rank  = rank.replace(' ',"")    
            for square_file,square_content in enumerate(rank):
                if square_content != '-':
                    piece_type = piece_symbols[square_content.lower()]
                    piece_color = "white" if square_content.upper() == square_content else "black"
                    piece_position =  self.get_square(square_file,square_rank)

                    self.pieces_in_play.append(Piece(piece_type,piece_color,piece_position))

    def display(self,board_in_text_format,square):
        board_in_text_format =  ''.join(board_in_text_format.splitlines())
        ranks = [board_in_text_format[start_index:start_index+15] for start_index in range(0,len(board_in_text_format),15)]
        occupied_squares = [piece.position for piece in self.pieces_in_play]
        if square in occupied_squares: squares_to_paint  = self.pieces_in_play[occupied_squares.index(square)].possible_moves
        
        for square_rank,rank in enumerate(ranks):
            rank  = rank.replace(' ',"")    
            for square_file,square_content in enumerate(rank):
                piece_position =  self.get_square(square_file,square_rank)
                color = 95 if piece_position in squares_to_paint else 90
                if piece_position[0] == 'h':
                    print(f"\033[{color}m{square_content}\033[m",end="\n")
                else :
                    print(f"\033[{color}m{square_content}\033[m",end=" ")

        

    def get_square(self,x,y):
        return self.POSITIONS[(y*8)+x]

    def create_screen(self,dimensions):
        self.SCREEN = pygame.display.set_mode(dimensions)
        pygame.display.set_caption("Chess game")

    def get_coordinates(self,square):
        square_x = int(ord(square[0])-97)
        square_y = abs(int(square[1]) - 8)
        return square_x,square_y
    
    def predict_moves(self,selected_piece):
        board_matrix = [self.POSITIONS[index:index+8] for index in range(0,len(self.POSITIONS),8)]
        occupied_squares = [piece.position for piece in self.pieces_in_play ]
        selected_piece_x,selected_piece_y = self.get_coordinates(selected_piece.position) 

        if selected_piece.movement_type == "continous":
            action_range = 7
        elif selected_piece.type == "pawn" and selected_piece.times_moved == 0:
            action_range = 2
        else:
            action_range = 1

        for direction in selected_piece.movement_direction:
            for distance in range(1,action_range+1):
                new_x  = selected_piece_x + distance * direction[0]
                new_y  = selected_piece_y + distance * direction[1]
                if new_x in range(8) and new_y in range(8):
                    new_square = self.get_square(new_x,new_y)
                    if new_square in occupied_squares:
                        piece_on_new_square = self.pieces_in_play[occupied_squares.index(new_square)]
                        if selected_piece.color == piece_on_new_square.color:
                            selected_piece.protecting.append(piece_on_new_square)
                            piece_on_new_square.protected_by.append(selected_piece)
                            break
                        else: #if the color is not the same then it can capture it
                            selected_piece.attacking.append(piece_on_new_square)
                            piece_on_new_square.attacked_by.append(selected_piece)
                            selected_piece.possible_moves.append(new_square)
                            break
                    else: #if the new square is empty
                        selected_piece.possible_moves.append(new_square)


        
        

    def move_piece(self):
        pass
    def check(self):
        pass
    def checkmate(self):
        pass
    def stalemate(self):
        pass
    def check_for_exeptions(self):
        pass
    def switch_turn(self):
        pass 

"""
class Dot(pygame.sprite.Sprite):
    def __init__(self,specified_x,specified_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Assets\\dot.png"), (64,64))
        self.DOT_SIZE = self.image.get_width()
        self.adjustement = (64 - self.DOT_SIZE) // 2
        self.rect = (specified_x + self.adjustement,specified_y + self.adjustement,self.DOT_SIZE,self.DOT_SIZE)


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size,color,specified_x,specified_y,width, height):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("Arial", size)
        self.textSurface = self.font.render(text,True,color)
        self.image = pygame.Surface((width, height))

        self.rect = (specified_x,specified_y,width,height)
        W = self.textSurface.get_width()
        H = self.textSurface.get_height()

        ###need to turn text into a image
"""