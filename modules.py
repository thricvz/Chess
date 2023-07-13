import pygame 
from math import sqrt,pow
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
        self.capture_direction = Piece._movement_axis_map[self.type] if self.type != "pawn" else [[-1, -1], [1, -1]]
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

    def predict_moves(self,selected_piece):
        board_matrix = [self.POSITIONS[index:index+8] for index in range(0,len(self.POSITIONS),8)]
        occupied_squares = [piece.position for piece in self.pieces_in_play ]
        predicted_moves = []
        selected_piece_x,selected_piece_y = self._get_coordinates(selected_piece.position) 

        if selected_piece.movement_type == "continous":
            action_range = 7
        elif selected_piece.type == "pawn" and selected_piece.times_moved == 0:
            action_range = 2
        else:
            action_range = 1



        if selected_piece.color == "black": selected_piece.movement_direction = self._inverse_direction(selected_piece.movement_direction)

        for direction in selected_piece.movement_direction:
            for distance in range(1,action_range+1):
                new_x  = selected_piece_x + distance * direction[0]
                new_y  = selected_piece_y + distance * direction[1]
                if new_x in range(8) and new_y in range(8):
                    new_square = self._get_square(new_x,new_y)
                    if new_square in occupied_squares:
                        piece_on_new_square = self.pieces_in_play[occupied_squares.index(new_square)]

                        if selected_piece.color != piece_on_new_square.color and not(selected_piece.type == piece_on_new_square.type == "king"):
                            selected_piece.attacking.append(piece_on_new_square)
                            piece_on_new_square.attacked_by.append(selected_piece)
                            predicted_moves.append(new_square)
                            break
                        else: 
                            selected_piece.protecting.append(piece_on_new_square)
                            piece_on_new_square.protected_by.append(selected_piece)
                            break
                    else: #if the new square is empty
                        predicted_moves.append(new_square)

        #pawn capture mechanic 
        if selected_piece.type == "pawn":
                pawn_capture_direction = [[-1, -1], [1, -1]]
                if selected_piece.color == "black": selected_piece.capture_direction = self._inverse_direction(selected_piece.capture_direction)

                for index_direction,direction in enumerate(selected_piece.capture_direction):
                    new_x  = selected_piece_x +  direction[0]
                    new_y  = selected_piece_y +  direction[1]

                    if new_x in range(8) and new_y in range(8):
                        new_square = self._get_square(new_x,new_y)
                        if new_square in occupied_squares:
                            piece_on_new_square = self.pieces_in_play[occupied_squares.index(new_square)]
                            if selected_piece.color != piece_on_new_square.color:
                                selected_piece.attacking.append(piece_on_new_square)
                                piece_on_new_square.attacked_by.append(selected_piece)
                                predicted_moves.append(new_square)
                            else:
                                selected_piece.protecting.append(piece_on_new_square)
                                piece_on_new_square.protected_by.append(selected_piece)
        return predicted_moves
    
    def predict_capture(self,selected_piece):
        board_matrix = [self.POSITIONS[index:index+8] for index in range(0,len(self.POSITIONS),8)]
        capture_squares = []
        selected_piece_x,selected_piece_y = self._get_coordinates(selected_piece.position) 

        if selected_piece.movement_type == "continous":
            action_range = 7
        else:
            action_range = 1



        if selected_piece.color == "black": selected_piece.capture_direction = self._inverse_direction(selected_piece.capture_direction)

        for direction in selected_piece.capture_direction:
            for distance in range(1,action_range+1):
                new_x  = selected_piece_x + distance * direction[0]
                new_y  = selected_piece_y + distance * direction[1]
                if new_x in range(8) and new_y in range(8):
                    new_square = self._get_square(new_x,new_y)
                    capture_squares.append(new_square)
        
        return capture_squares

    def update_pieces_statuses(self):
        for piece in self.pieces_in_play:
            piece.possible_moves = self.predict_moves(piece)
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
        king =  next((piece for piece in player_pieces if piece.type == 'king'),None)
        return (len(king.attacked_by) > 0)
    

    def check_escape_options(self,player):
        player_pieces = self._get_player_pieces(player)
        oponent_pieces = self._get_player_pieces(self.players[self.players.index(player)-1])
        king =  next((piece for piece in player_pieces if piece.type == 'king'),None)
        king_attacker =  king.attacked_by[0] #king can't be attacked by two pieces simultaneosly
        check_escape_options = []
        ##resets all moves to only accept those that prevent check
        for player_piece in player_pieces: player_piece.possible_moves.clear()

        #first method : fleeing
        ilegal_squares = []
        for oponent_piece in oponent_pieces: 
            capture_squares = self.predict_capture(oponent_piece)
            ilegal_squares.extend(capture_squares)
        
        king.possible_moves = self.predict_moves(king)
        king.possible_moves = [move for move in king.possible_moves if move not in ilegal_squares]

        if len(king.possible_moves): check_escape_options.append("move king")

        #second method : capturing attacking piece
        if len(king_attacker.protected_by) > 1 :
            #the king can no longer capture its attacker (filters the king out)
            king_attacker.attacked_by = [piece for piece in king_attacker.attacked_by if piece.type != "king"]
        
        if len(king_attacker.attacked_by) > len(king_attacker.protected_by):
            for piece_able_to_capture_attacker in king_attacker.attacked_by:
                piece_able_to_capture_attacker.possible_moves.append(king_attacker.position)
            
            check_escape_options.append("capture attacker")
    
        ###third method : blocking 
        #  
        #calculate the distance between pieces pythagore theorem(distance here is the number of squares in between the pieces)
        king_attacker_x,king_attacker_y = self._get_coordinates(king_attacker.position)
        king_x,king_y = self._get_coordinates(king.position)
        distance_x_axis = king_attacker_x - king_x - 1
        distance_y_axis = king_attacker_y - king_y - 1
        distance = int(sqrt(pow(distance_x_axis,2)+pow(distance_y_axis,2)))
        

        if king_attacker.movement_type == "continous" and distance > 0:
            attack_line = []
            #attacking line is vertical
            if king_attacker.position[0]  == king.position[0] : #pieces on same file
                piece_on_lowest_rank,piece_on_highest_rank = (king_attacker,king) if king_attacker.position[1] < king.position[1] else (king,king_attacker)
                for rank_increment in range(1,distance):
                    attack_line.append(f"{piece_on_lowest_rank.position[0]}{int(piece_on_lowest_rank.position[1])+rank_increment}")
            #attack_line is horizontal
            elif  king_attacker.position[1]  == king.position[1]:
                piece_on_lowest_file,piece_on_highest_file = (king_attacker,king) if king_attacker.position[0] < king.position[0] else (king,king_attacker)
                for file_increment in range(1,distance):
                    file_index = int(ord(piece_on_lowest_file.position[0])-97) + file_increment
                    square = self._get_square(file_index,int(piece_on_lowest_file.position[1])) 
                    attack_line.append(square)

            #attacking line is diagonal
            else:
                piece_on_lowest_rank,piece_on_highest_rank = (king_attacker,king) if king_attacker.position[1] < king.position[1] else (king,king_attacker)
                diagonal_direction = [1,-1] #bottom left to top right
                if ord(piece_on_highest_rank.position[0]) - ord(piece_on_lowest_rank.position[0]) > 0:#if higghest piece is on the lowest pieces left side
                    diagonal_direction[0] *= -1 #changes the diagonal_direction of diagonal from bottom right to top left
                
                for increment in range(1,distance):
                    file_index = int(ord(piece_on_lowest_rank.position[0])-97) + increment * diagonal_direction[0]
                    rank_index = int(piece_on_lowest_rank.position[1]) + increment * diagonal_direction[1]
                    square = self._get_square(file_index,rank_index)
                    attack_line.append(square)

            ##checking for pieces that can block the line 
            for piece in player_pieces:
                previous_moves_not_to_overwrite = piece.possible_moves
                legal_moves = []
                piece.possible_moves = self.predict_moves(piece)
                for square in piece.possible_moves:
                    if square in attack_line:
                        legal_moves.append(square)
                
                piece.possible_moves.clear()
                piece.possible_moves.extend(legal_moves)
                piece.possible_moves.extend(previous_moves_not_to_overwrite)
                if len(legal_moves): check_escape_options.append("block attack")

        return check_escape_options

    def checkmate(self,player):
        print(self.check_escape_options(player))
        if self.player_in_check(player) and not len(self.check_escape_options(player)): #if way to prevent king capture
            return True
        else:
            return False
        
        
    def stalemate(self,player):
        if not self.player_in_check(player):
            player_pieces = self._get_player_pieces(player)
            legal_moves  = []
            for piece in player_pieces:
                legal_moves.extend(piece.possible_moves)

            return True if not len(legal_moves) else False
        else:
            return False
        
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