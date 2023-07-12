import pygame 

class Piece(pygame.sprite.Sprite):
    _movement_axis_map = {
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
        self.movement_direction = Piece._movement_axis_map[self.type]
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
                if square_content != '.':
                    piece_type = piece_symbols[square_content.lower()]
                    piece_color = "white" if square_content.upper() == square_content else "black"
                    piece_position =  self._get_square(square_file,square_rank)

                    self.pieces_in_play.append(Piece(piece_type,piece_color,piece_position))
        return None 

    def display(self,focused_square=None):
        empty_board = [["." for _file in range(8)] for _rank in range(8)]
        symbols_to_black_pieces = {'k': '♔','q': '♕','r': '♖','b': '♗','n': '♘','p': '♙'}
        symbols_to_white_pieces = {'k': '♚','q': '♛','r': '♜','b': '♝','n': '♞','p': '♟'}
        squares_to_replace = self._get_occupied_squares() #the square contains a piece by default
        #places every piece on board
        for square in squares_to_replace:
            square_x,square_y = self._get_coordinates(square)
            piece_on_square = self.pieces_in_play[squares_to_replace.index(square)]
            #filter the input for the dictionnary
            piece_on_square_symbol = piece_on_square.type[0] if piece_on_square.type != "knight" else piece_on_square.type[1]
            #apply changes to board
            if piece_on_square.color == "black" :
                empty_board[square_y][square_x] = symbols_to_black_pieces[piece_on_square_symbol]
            else :
                empty_board[square_y][square_x] = symbols_to_white_pieces[piece_on_square_symbol]

        squares_to_paint = []
        if focused_square != None:
            if focused_square in squares_to_replace: squares_to_paint = self.pieces_in_play[squares_to_replace.index(focused_square)].possible_moves

        for rank_index,rank in enumerate(empty_board):
            for file_index in range(len(rank)):
                square_content = empty_board[rank_index][file_index]
                square = self._get_square(file_index,rank_index)

                color = 95 if square in squares_to_paint else 90 
                print(f"\033[{color}m{square_content}\033[m",end=" ")
            print("",end="\n")

        return None
        
    def _get_occupied_squares(self):
        return [piece.position for piece in self.pieces_in_play ]
    
    def _get_player_pieces(self,player):
        return [piece for piece in self.pieces_in_play if piece.color == player]
    
    def _get_square(self,x,y):
        return self.POSITIONS[(y*8)+x]

    def _get_coordinates(self,square):
        square_x = int(ord(square[0])-97)
        square_y = abs(int(square[1]) - 8)
        return square_x,square_y
    
    def create_screen(self,dimensions):
        self.SCREEN = pygame.display.set_mode(dimensions)
        pygame.display.set_caption("Chess game")
        return None

    def _inverse_direction(self,directions_list):
        for direction_index,direction in enumerate(directions_list):
            directions_list[direction_index] = [direction[0]*-1,direction[1]*-1]
        return directions_list

    def predict_moves(self,selected_piece,capture_only_mode = False):
        board_matrix = [self.POSITIONS[index:index+8] for index in range(0,len(self.POSITIONS),8)]
        occupied_squares = [piece.position for piece in self.pieces_in_play ]
        selected_piece_x,selected_piece_y = self._get_coordinates(selected_piece.position) 

        if selected_piece.movement_type == "continous":
            action_range = 7
        elif selected_piece.type == "pawn" and selected_piece.times_moved == 0:
            action_range = 2
        else:
            action_range = 1


        if selected_piece.type == "pawn":
                pawn_capture_direction = [[-1, -1], [1, -1]]
                if selected_piece.color == "black": pawn_capture_direction = self._inverse_direction(pawn_capture_direction)

                selected_piece.movement_direction = pawn_capture_direction

                for index_direction,direction in enumerate(selected_piece.movement_direction):
                    new_x  = selected_piece_x +  direction[0]
                    new_y  = selected_piece_y +  direction[1]

                    if new_x in range(8) and new_y in range(8):
                        new_square = self._get_square(new_x,new_y)
                        if capture_only_mode:
                            selected_piece.possible_moves.append(new_square)
                            if index_direction == 1: return None #sets the loop to an end

                        if new_square in occupied_squares:
                            piece_on_new_square = self.pieces_in_play[occupied_squares.index(new_square)]
                            if selected_piece.color != piece_on_new_square.color:
                                selected_piece.attacking.append(piece_on_new_square)
                                piece_on_new_square.attacked_by.append(selected_piece)
                                selected_piece.possible_moves.append(new_square)
                            else:
                                selected_piece.protecting.append(piece_on_new_square)
                                piece_on_new_square.protected_by.append(selected_piece)

        if selected_piece.color == "black": selected_piece.movement_direction = self._inverse_direction(selected_piece.movement_direction)

        for direction in selected_piece.movement_direction:
            for distance in range(1,action_range+1):
                new_x  = selected_piece_x + distance * direction[0]
                new_y  = selected_piece_y + distance * direction[1]
                if new_x in range(8) and new_y in range(8):
                    new_square = self._get_square(new_x,new_y)
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

        #pawn capture mechanic 
        return None

            

    def update_pieces_statuses(self):
        for piece in self.pieces_in_play:
            self.predict_moves(piece)
        return None
        
    def switch_turn(self):
        self.players.reverse()
        self.turn = self.players[0]
        return None

    def move_piece(self,piece,destination_square):
        if destination_square not in piece.possible_moves:
            return "please enter a valid position"
        else:
            occupied_squares = [piece.position for piece in self.pieces_in_play ]
            if destination_square in occupied_squares: self.pieces_in_play.pop(occupied_squares.index(destination_square))#deletes the enemy piece on the square 
            piece.position = destination_square
            return None
            
    def player_in_check(self,player):
        player_pieces = self._get_player_pieces(player)
        players_king =  next((piece for piece in player_pieces if piece.type == 'king'),None)
        return (len(players_king.attacked_by) > 0)

    def options_out_of_check(self,player):
        player_pieces = self._get_player_pieces(player)
        openent_pieces = self._get_player_pieces(self.players.index(player)-1)
        players_king =  next((piece for piece in player_pieces if piece.type == 'king'),None)
        king_attacker =  players_king.attacked_by[0] #king can't be attacked by two pieces simultaneosly
        options_out_of_check = []
        ##resets all moves to only accept those that prevent check
        for player_piece in player_pieces: player_piece.possible_moves  = []

        #first method : fleeing
        if king_attacker.movement_type == "continous":
            pass
           ##checks for every piece in kings pos

        #second method : capturing attacking piece
        if len(king_attacker.protected_by) > 1 :
            #the king can no longer capture its attacker (filters the king out)
            king_attacker.attacked_by = [piece for piece in king_attacker.attacked_by if piece.type != "king"]
        
        if len(king_attacker.attacked_by) > len(king_attacker.protected_by):
            for piece_able_to_capture_attacker in king_attacker.attacked_by:
                piece_able_to_capture_attacker.possible_moves.append(king_attacker.position)
            
            options_out_of_check.append("capturing attacker")
    
        #third method : fleeing  
        for oponent_piece in openent_pieces: self.predict_moves(oponent_piece,capture_only_mode=True)
        ilegal_squares =  [oponent_piece.possible_moves for oponent_piece in openent_pieces]
        self.predict_moves(players_king)
        players_king.possible_moves = [move for move in players_king.possible_moves if move not in ilegal_squares]
        if len(players_king.possible_moves) : options_out_of_check.append["move king"]



            


    def checkmate(self):
        pass
    def stalemate(self):
        pass
    def check_for_exeptions(self):
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