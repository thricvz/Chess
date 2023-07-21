from modules import Board
from graphic_interface import GUI
import pygame

initial_board = """
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
"""

pygame.init()
#staring essential elements of game
GUI = GUI((512,512))
CLOCK = pygame.time.Clock()
board = Board()
running = True
piece_was_selected = False
board.build_from_text(initial_board)
GUI.create_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            raise SystemExit

    
        GUI.display_pieces()
    
        board.update_pieces_statuses()
    
        if board.checkmate(board.turn):
            GUI.display_message(f"{board.turn} lost",board.turn)
            running = False
            raise SystemExit
        
        if board.stalemate(board.turn) or board.only_kings_left(board.turn):
            GUI.display_message(f"Draw",board.turn)
            running = False
            raise SystemExit
        
        if board.player_in_check(board.turn):
            GUI.display_message("check",board.turn)
            board.check_escape_options(board.turn)
    
        castle_possible = board.castle_options(board.turn) > 0
        en_passant_possible = board.en_passant(board.turn)
    
        if piece_was_selected :
            GUI.update_predicted_squares(selected_piece.possible_moves)
            destination_square = GUI.get_clicked_square(event)
    
            if destination_square != "undefined":
                if destination_square == selected_square: #unselects the piece
                    piece_was_selected = False
                    GUI.reset_predicted_squares()
                    
                elif destination_square in selected_piece.possible_moves:
                    board.move_piece(selected_piece,destination_square)
                    promotion = board.pawn_promotion(selected_piece)
                    #checks for all special moves
                    if promotion:board.promote_pawn(selected_piece,"queen") 
                    if castle_possible  and selected_piece.type == "king" : board.castle(selected_piece)
                    if en_passant_possible and selected_piece.type == "pawn" : board.en_passant_capture(selected_piece)
                        
                    GUI.reset_predicted_squares()
                    GUI.reset_pieces()
                    board.switch_turn()
                    board.update_en_passant_possiblity()
                    board.reset_piece_statuses()
                    piece_was_selected = False
                    selected_square = None
                else :
                    pass
        else :
            GUI.display_message(f"{board.turn}'s turn",board.turn)
            selected_square = GUI.get_clicked_square(event)
            if selected_square != "undefined":
                if selected_square in [piece.position for piece in board._get_player_pieces(board.turn)]:
                    piece_was_selected = True
                    selected_piece =  [piece for piece in board._get_player_pieces(board.turn) if piece.position == selected_square][0]
        
        GUI.update_pieces(board.pieces_in_play)
        CLOCK.tick(60)
        pygame.display.update()
        
pygame.time.wait(10000)
pygame.quit()