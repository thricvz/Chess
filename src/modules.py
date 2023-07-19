from math import sqrt,pow

class Piece():
    ###this format consists of the "steps" that have to be done on the board (x,y) : ex-> (-1,1) would be one "step" to the left and one "step" to the bottom
    _movement_axis_map = {
                    "pawn": [[0,-1]],
                    "rook" : [[1,0],[0,-1],[-1,0],[0,1]],
                    "knight" : [[-2,1],[-1,2],[-2,-1],[-1,-2],[2,1],[1,2],[2,-1],[1,-2]],
                    "bishop" : [[-1,1],[-1,-1],[1,1],[1,-1]] ,
                    "queen" : [[1,0],[0,-1],[-1,0],[0,1],[-1,1],[-1,-1],[1,1],[1,-1]],
                    "king" : [[1,0],[0,-1],[-1,0],[0,1],[-1,1],[-1,-1],[1,1],[1,-1]]
                          }
    def __init__(self,type,color,position):
        """Generates a new piece object based on color ,type and positon.

        :param color: piece color
        :type color: string
        :param type: piece type
        :type: string
        :param positon: piece initial_position
        :type: string
        """
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
        if self.type == "pawn" : 
            self.en_passant_possibility_right = True
            self.en_passant_possibility_left = True
        self.exception = None
        self.times_moved = 0
        

#Board Class
class Board(Piece):
    """This is a class responsible for managing all events of the game."""
    
    def __init__(self):
        self.POSITIONS = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.players = ["white","black"]
        self.pieces_in_play = []
        self.turn = self.players[0]
        self.previous_turn = None

    def build_from_text(self,board_in_text_format):
        """This function goes trough a board expressed in text format,where a piece is represented by a specific letter
        either capitalized or not(determines the color of the piece,by default black for lower case and white for a capitalized case)
        and generates a new piece object as well as the function adds this new object to the list of pieces in play.

        :param board_in_text_format: game board in text format
        :type board_in_text_format: string
        :return:  None
        """

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

    def display(self,focused_square = None):
        """Displays the current board in terminal,by specifying a unempty square of the board
        it displays the available moves for the piece on that square.

        :param focused_square: square to display available moves
        :type focused_square: str 
        :return: None
        """
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
        if focused_square is not None:
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
        """Gathers all squares on board that host a piece.
        
        :return: all occupied squares
        :rtype: list
        """
        return [piece.position for piece in self.pieces_in_play ]
    
    def _get_player_pieces(self,player):
        """Gathers all pieces belonging to a specific player.
        
        :param player: player (either "black" or "white")
        :type player: string
        :return: all pieces belonging to player
        :rtype: list
        """

        return [piece for piece in self.pieces_in_play if piece.color == player]
    
    def _get_square(self,x,y):
        """Transforms x and y coordinates into their corresponding square on the board.*
        Please NOTE that both coordinates must be in the range of 0 to 7.

        :param x: x coordinate
        :type x: integer
        :param y: y coordinate
        :type y: integer
        :return: square on the board
        :rtype: string
        """

        return self.POSITIONS[(y*8)+x]

    def _get_coordinates(self,square):
        """ Transforms a square of the board into its corresponding x and y coordinates.*
        Please NOTE that the square must exist on the board.

        
        :param square: square on the board
        :type square: string
        :return: x and y coordinates
        :rtype: tuple
        """
         
        square_x = int(ord(square[0])-97)
        square_y = abs(int(square[1]) - 8)
        return square_x,square_y


    def _inverse_direction(self,directions_list):
        """ Gets the set of movement_directions belonging to a piece and reverses the  original direction.

        :param directions_list: set of movement_directions
        :type directions_list: list
        :return: inverted set of movemement_directions
        :rtype: list
        """
        inversed_direction_list = []
        for direction in directions_list:
            inversed_direction_list.append([direction[0]*-1,direction[1]*-1])
        return inversed_direction_list

    def predict_moves(self,selected_piece):
        """
        Predicts all possible movements for a piece without checking if the move is legal.

        :param selected_piece: Piece that moves should be generated
        :type selected_piece: class
        :return: list of all possible moves 
        :rtype: list
        """

        board_matrix = [self.POSITIONS[index:index+8] for index in range(0,len(self.POSITIONS),8)]
        movement_direction = selected_piece.movement_direction
        occupied_squares = [piece.position for piece in self.pieces_in_play ]
        predicted_moves = []
        selected_piece_x,selected_piece_y = self._get_coordinates(selected_piece.position) 

        if selected_piece.movement_type == "continous":
            action_range = 7
        elif selected_piece.type == "pawn" and selected_piece.times_moved == 0:
            action_range = 2
        else:
            action_range = 1

        if selected_piece.color == "black": movement_direction = self._inverse_direction(selected_piece.movement_direction)
        for direction in movement_direction:
            for distance in range(1,action_range+1):
                new_x  = selected_piece_x + distance * direction[0]
                new_y  = selected_piece_y + distance * direction[1]
                if new_x in range(8) and new_y in range(8):
                    new_square = self._get_square(new_x,new_y)
                    piece_on_new_square = self.pieces_in_play[occupied_squares.index(new_square)] if new_square in occupied_squares else None
                    
                    if piece_on_new_square is None:
                        predicted_moves.append(new_square)
                    
                    elif selected_piece.color != piece_on_new_square.color and not(selected_piece.type == piece_on_new_square.type == "king") and selected_piece.type != "pawn":
                        selected_piece.attacking.append(piece_on_new_square)
                        piece_on_new_square.attacked_by.append(selected_piece)
                        predicted_moves.append(new_square)
                        break
                    elif selected_piece.type != "pawn": 
                        selected_piece.protecting.append(piece_on_new_square)
                        piece_on_new_square.protected_by.append(selected_piece)
                        break
                    else:
                        break
                else:
                    break
                
        #pawn capture mechanic 
        if selected_piece.type == "pawn":
                pawn_capture_direction = [[-1, -1], [1, -1]]
                if selected_piece.color == "black": pawn_capture_direction = self._inverse_direction(pawn_capture_direction)

                for index_direction,direction in enumerate(pawn_capture_direction):
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
    
    def predict_capture(self,selected_piece,ignore_occupied_squares = True):
        """
        Predicts all squares that a piece exerces a threat on.

        :param selected_piece: Piece that capture positions should be generated
        :type selected_piece: class
        :return: list of all capture positions
        :rtype: list
        """
        board_matrix = [self.POSITIONS[index:index+8] for index in range(0,len(self.POSITIONS),8)]
        occupied_squares = self._get_occupied_squares()
        capture_direction = selected_piece.capture_direction
        capture_squares = []
        selected_piece_x,selected_piece_y = self._get_coordinates(selected_piece.position) 

        if selected_piece.movement_type == "continous":
            action_range = 7
        else:
            action_range = 1
            
        if selected_piece.color == "black": capture_direction = self._inverse_direction(selected_piece.capture_direction)

        for direction in capture_direction:
            for distance in range(1,action_range+1):
                new_x  = selected_piece_x + distance * direction[0]
                new_y  = selected_piece_y + distance * direction[1]
                if new_x in range(8) and new_y in range(8):
                    new_square = self._get_square(new_x,new_y)
                    if selected_piece.type != "pawn" and not ignore_occupied_squares and new_square in occupied_squares: break
                    capture_squares.append(new_square)
        
        return capture_squares
    
    def reset_piece_statuses(self):
        """
        Resets all pieces attributes.

        :return: None
        """
        for piece in self.pieces_in_play:
            piece.attacked_by.clear()
            piece.attacking.clear()
            piece.protected_by.clear()
            piece.protecting.clear() 
            piece.possible_moves.clear()
        return None
        
    def update_pieces_statuses(self):
        """
        Updates all piece attributes,and possible moves taking in consideration if those are legal or not
        
        :return: None
        """
        #resets every piece but updates its position
        for piece in self.pieces_in_play:
            piece.attacked_by = list(set(piece.attacked_by))
            piece.attacking = list(set(piece.attacking))
            piece.protected_by = list(set(piece.protected_by))
            piece.protecting = list(set(piece.protecting))
            piece.possible_moves = list(self.predict_moves(piece))
            
        for piece in self.pieces_in_play : 
            self.restrict_piece_movement(piece)
        
        return None
        
    def switch_turn(self):
        """
        Switches the turn.
        
        :return: None
        """
        self.players.reverse()
        self.previous_turn = self.turn
        self.turn = self.players[0]
        return None

    def move_piece(self,piece,destination_square):
        """
        Moves a piece to the specified square.
        
        :param piece: Piece to move
        :type piece: class
        :param destination_square: destination square
        :type destination_square: string
        :return: None
        """
        if destination_square not in piece.possible_moves:
            return "please enter a valid position"
        else:
            occupied_squares = [piece.position for piece in self.pieces_in_play ]
            if destination_square in occupied_squares: self.pieces_in_play.pop(occupied_squares.index(destination_square))#deletes the enemy piece on the square 
            piece.position = destination_square
            piece.times_moved += 1
            return None
            
    def player_in_check(self,player):
        """
        Idicates if the player has been put under check.
        
        :param player: specified player
        :type player: string
        :return: None
        :rtype: boolean
        """
         
        player_pieces = self._get_player_pieces(player)
        king =  next((piece for piece in player_pieces if piece.type == 'king'),None)
        return len(king.attacked_by) > 0 
    
    def _get_attack_line(self,attacker,victim):
        """
        Return the attack line between the pieces.NOTE that the pieces
        must be on a common line(diagonal,horizontal or vertical).

        :param attacker: Piece attacking 
        :type attacker: class
        :param victim: Piece being attacked
        :type victim: class
       
        :return: a list of squares between both pieces
        :rtype: list
        """
        attacker_x,attacker_y = self._get_coordinates(attacker.position)
        victim_x,victim_y = self._get_coordinates(victim.position)
        distance_x_axis = abs(attacker_x - victim_x)-1 
        distance_y_axis = abs(attacker_y - victim_y)-1
        distance = sqrt(pow(distance_x_axis,2)+pow(distance_y_axis,2))
        attack_line = []
        

        if attacker.movement_type == "continous" and distance > 0:
            #attack line is vertical
            if attacker.position[0]  == victim.position[0] : #pieces on same file
                piece_on_lowest_rank,piece_on_highest_rank = (attacker,victim) if attacker.position[1] < victim.position[1] else (victim,attacker)
                file_index,rank_index = self._get_coordinates(piece_on_lowest_rank.position)
                for rank_increment in range(1,distance_y_axis+1):
                    new_rank_index = rank_index + rank_increment
                    if new_rank_index in range(8):
                        square = self._get_square(file_index,new_rank_index) 
                        attack_line.append(square)

            #attack_line is horizontal
            elif  attacker.position[1]  == victim.position[1]:
                piece_on_lowest_file,piece_on_highest_file = (attacker,victim) if attacker.position[0] < victim.position[0] else (victim,attacker)
                file_index,rank_index = self._get_coordinates(piece_on_lowest_file.position)
                for file_increment in range(1,distance_x_axis+1):
                    new_file_index = file_index + file_increment
                    if new_file_index in range(8):
                        square = self._get_square(new_file_index,rank_index) 
                        attack_line.append(square)
            #attacvictim line is diagonal
            else:
                piece_on_lowest_rank,piece_on_highest_rank = (attacker,victim) if attacker.position[1] < victim.position[1] else (victim,attacker)
                diagonal_direction = [1,-1] #bottom left to top right
                if ord(piece_on_highest_rank.position[0]) - ord(piece_on_lowest_rank.position[0])*-1 > 0:#if higghest piece is on the lowest pieces left side
                    diagonal_direction[0] *= -1 #changes the diagonal_direction of diagonal from bottom right to top left
                
                distance_diagonal = distance_x_axis #in this case both distances are equal
                file_index,rank_index = self._get_coordinates(piece_on_lowest_rank.position)

                for increment in range(1,distance_diagonal):
                    new_file_index = file_index + increment * diagonal_direction[0]
                    new_rank_index = rank_index + increment * diagonal_direction[1]
                    if new_file_index in range(8) and new_rank_index in range(8):
                        square = self._get_square(new_file_index,new_rank_index)
                        attack_line.append(square)
                   
        return attack_line
    
    def check_escape_options(self,player):
        """
        Returns all possible options in order to escape from check.NOTE that the player must be under check
        once you call this method.
        
        :param player: specified player
        :type player: string
        :return: all available options to get player out of check
        :rtype: list
        """
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
        if len(king_attacker.protected_by):
            #the king can no longer capture its attacker (filters the king out)
            king_attacker.attacked_by = [piece for piece in king_attacker.attacked_by if piece.type != "king"]
        
        if len(king_attacker.attacked_by) >= len(king_attacker.protected_by) and len(king_attacker.attacked_by):
            for piece_able_to_capture_attacker in king_attacker.attacked_by:
                piece_able_to_capture_attacker.possible_moves.append(king_attacker.position)
            
            check_escape_options.append("capture attacker")
    
        ###third method : blocking 
        attack_line = self._get_attack_line(king_attacker,king)
        ##checking for pieces that can block the line 
        for piece in player_pieces:
            if piece.type != "king":
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

        return list(set(check_escape_options))
    

    def restrict_piece_movement(self,piece):
        """Deletes all ilegal moves from a piece's list of possible moves.
        
        :param piece: Piece to check for legal moves
        :type piece: class
        :return: None
        """
        player = piece.color
        if piece.type == "king":
            oponent_pieces = self._get_player_pieces(self.players[self.players.index(player)-1])
            for oponent_piece in oponent_pieces:
                for oponent_move in self.predict_capture(oponent_piece,ignore_occupied_squares=False):
                    if oponent_move in piece.possible_moves: piece.possible_moves.remove(oponent_move)
                    if oponent_piece.position in piece.possible_moves and len(oponent_piece.protected_by) : piece.possible_moves.remove(oponent_piece.position)
        else:
            piece_attackers = piece.attacked_by
            king = [ally_piece for ally_piece in self.pieces_in_play if ally_piece.color == piece.color and ally_piece.type == "king" ][0]
            if len(piece_attackers):
                for attacker in piece_attackers:
                    if attacker.movement_type == "continous" and king.position in self.predict_capture(attacker):
                        piece_possible_moves_copy = piece.possible_moves.copy()
                        piece.possible_moves.clear()
                        attack_line = self._get_attack_line(attacker,king)
                        for move in piece_possible_moves_copy:
                            if move in attack_line or move == attacker.position: piece.possible_moves.append(move)
                            #if  move == attacker.position : piece.possible_moves.append(move)
                    
            
        return None
    
    def checkmate(self,player):
        """
        Idicates if the player has been mated.
        
        :param player: specified player
        :type player: string
        :return: None
        :rtype: boolean
        """
        #print(self.check_escape_options(player))
        if self.player_in_check(player) and not len(self.check_escape_options(player)): #if way to prevent king capture
            return True
        else:
            return False
        
    def stalemate(self,player):
        """
        Idicates if the player has been stalemated.
        
        :param player: specified player
        :type player: string
        :return: None
        :rtype: boolean
        """
        player_pieces = self._get_player_pieces(player)
        legal_moves = []
        for piece in player_pieces: legal_moves.extend(piece.possible_moves)
        return True if not self.player_in_check(player) and not len(legal_moves) else False

        
    def castle_options(self,player):
        """
        Returns the number of options a player has to castle.
        
        :param player: specified player
        :type player: string
        :return: number of castle options
        :rtype: int
        """
        player_pieces = self._get_player_pieces(player)
        castle_options = 0
        oponent_pieces = self._get_player_pieces(self.players[self.players.index(player)-1])
        rooks = [piece for piece in player_pieces if piece.type == "rook"]
        king  = [piece for piece in player_pieces if piece.type == "king"][0]
        if not len(rooks):  return castle_options
        for rook in rooks:
            rook.possible_moves = self.predict_moves(rook)
            squares_between_pieces = [position for position in rook.possible_moves if position[1] == rook.position[1]]

            oponent_attacking_squares = []
            for piece in oponent_pieces:
                oponent_attacking_squares.extend(self.predict_moves(piece))

            space_between_pieces = king in rook.protecting
            squares_in_between_under_attack = len(set(squares_between_pieces) & set(oponent_attacking_squares)) > 0
            king_in_check = self.player_in_check(player)
            pieces_at_original_position = king.times_moved == rook.times_moved == 0

            if pieces_at_original_position and space_between_pieces and not squares_in_between_under_attack and not king_in_check:
                squares_between_pieces.reverse()
                square_to_realise_castle = squares_between_pieces[1]
                king.possible_moves = self.predict_moves(king)
                king.possible_moves.append(square_to_realise_castle)
                castle_options += 1

        return castle_options
    
    def castle(self,king):
        """"
        Applies the changes to the board if the player has decided to castle.
        NOTE only call this function after verifying that the piece is a king and that it can castle.

        :param king: player's king 
        :type king: class
        :return: None
        """
        king_initial_pos = "e1" if king.color == "white" else "e8"
        initial_x,initial_y = self._get_coordinates(king_initial_pos)
        king_castle_position_left = self._get_square(initial_x-2,initial_y)
        king_castle_position_right = self._get_square(initial_x+2,initial_y)
        if king.position in king_castle_position_right:
            rooks_square = "h" + str(king.position[1])
            rook = [piece for piece in self.pieces_in_play if piece.position == rooks_square][0]
            rook.position = self._get_square(initial_x+1,initial_y)

        elif king.position in king_castle_position_left:
            rooks_square = "a" + str(king.position[1])
            rook = [piece for piece in self.pieces_in_play if piece.position == rooks_square][0]
            rook.position = self._get_square(initial_x-1,initial_y)
        else:
            print("no castling")
        
        return None
    
    def pawn_promotion(self,piece):
        """
        Returns if the specified piece can be promoted.
        
        :param piece: piece to check for promotion availability
        :type piece: class
        :return: promotion availability
        :rtype: boolean
        """
        if piece.type == "pawn" and (piece.color == "black" and piece.position[1] == "1") or (piece.color == "white" and piece.position[1] == "8"):
            return True
        return False
    
    def en_passant(self,player):
        """
        Returns if any of the players pieces can capture en passant.
        
        :param player: player
        :type player: string
        :return: player can capture en passant with any of his pieces
        :rtype: boolean
        """
        player_pawns = [piece for piece in self._get_player_pieces(player) if piece.type == "pawn"]
        for pawn in player_pawns:
            if len(self.en_passant_options_for_piece(pawn)):
                return True
        
        return False
    
    def en_passant_capture(self,piece):
        """"
        Applies the changes to the board if the player has decided to capture en passant.
        NOTE only call this function after verifying that the piece can capture en passant.

        :param piece: piece to capture en passant 
        :type piece: class
        :return: None
        """
        en_passant_direction = -1 if piece.color == "black" else 1
        piece_x,piece_y = self._get_coordinates(piece.position)
        piece_behind_square = self._get_square(piece_x,piece_y+ en_passant_direction)
        occupied_squares = self._get_occupied_squares()

        if piece_behind_square in occupied_squares:self.pieces_in_play.pop(occupied_squares.index(piece_behind_square))
        return None
    
    def en_passant_options_for_piece(self,piece,modify_piece_possible_moves = True):
        """
        Returns the all directions in which a pawn has to capture en passant.
        
        :param piece: piece to check for en passant possibility
        :type player: string
        :return: options for en passant capture
        :rtype: list
        """
        en_passant_options = []
        occupied_squares = self._get_occupied_squares()
        en_passant_direction = -1 if piece.color == "black" else 1
        specified_rank = "4" if piece.color == "black" else "5" 
        if piece.type == "pawn" and piece.position[1] == specified_rank:

                piece_x,piece_y = self._get_coordinates(piece.position)
                squares_next_to_piece = list()
                #gets all pieces next to the piece
                for increment_x in range(1,-2,-1):
                    if piece_x + increment_x in range(8):squares_next_to_piece.append(self._get_square(piece_x + increment_x,piece_y))
                squares_next_to_piece.remove(piece.position)
                
                for square_index,square in enumerate(squares_next_to_piece):
                    if square in occupied_squares:
                        neighbour_piece = self.pieces_in_play[occupied_squares.index(square)]
                        piece_en_passant_possible = piece.en_passant_possibility_left if square_index == 0 else piece.en_passant_possibility_right
                        if neighbour_piece.type == "pawn" and neighbour_piece.color != piece.color and neighbour_piece.times_moved == 1 and piece_en_passant_possible:
                            new_y = int(neighbour_piece.position[1]) + en_passant_direction
                            if modify_piece_possible_moves : piece.possible_moves.append(neighbour_piece.position[0]+str(new_y))
                            
                            side = "left" if square_index == 0 else "right"
                            en_passant_options.append(side)
        return en_passant_options

    def update_en_passant_possiblity(self):
        """
        Applies the rule according to which a pawn can only capture
        en passant during the turn the option has appeared.
        
        :return: None
        """
        if self.previous_turn != self.turn and self.previous_turn is not None:
            previous_player_pawns = [piece for piece in self._get_player_pieces(self.previous_turn) if piece.type == "pawn"]
            for pawn in previous_player_pawns : 
                en_passant_options =  self.en_passant_options_for_piece(pawn,modify_piece_possible_moves=False)
                if len(en_passant_options):
                    for option in en_passant_options:
                        if option == "right":
                            pawn.en_passant_possibility_right = False         
                        else:       
                            pawn.en_passant_possibility_left = False            
        return None
    
    def promote_pawn(self,pawn,desired_piece):
        """"
        Applies the changes to the board if the player has decided to promote the pawn.
        NOTE only call this function after verifying that the piece you pass in the function is a pawn and can be promoted.

        :param piece: pawn to promote 
        :type piece: class
        :param desired_piece: type of the piece to promote to 
        :type desired_piece: class
        :return: None
        """
        new_piece = Piece(desired_piece,pawn.color,pawn.position)
        self.pieces_in_play.remove(pawn)
        self.pieces_in_play.append(new_piece)
        return None
