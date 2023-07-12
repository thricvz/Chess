from modules import Board
import json
from emoji import emojize

def test_predict_function(test_board,selected_piece_color,selected_piece_type,selected_piece_position,expected_values):
    board =  Board()
    board.build_from_text(test_board)
    for piece in board.pieces_in_play:
        if piece.type == selected_piece_type and piece.color == piece.color and piece.position == selected_piece_position:
            selected_piece = piece

    board.predict_moves(selected_piece)
    possible_moves = selected_piece.possible_moves
    assert sorted(possible_moves) == sorted(expected_values),f"\033[91mreturned:{possible_moves}\033[m \033[92mexpected:{expected_values}\033[m"
    print(emojize("Passed :check_mark:"))

def test_check_function(test_board,player_color,expected_value):
    board = Board()
    board.build_from_text(test_board)
    board.update_pieces_statuses()
    assert str(board.player_in_check(player_color)) == expected_value,board.player_in_check(player_color)
    print(emojize("Passed :check_mark:"))

def test_check_escape(test_board,player_color,expected_value):
    board = Board()
    board.build_from_text(test_board)
    board.update_pieces_statuses()
    escape_options = board.check_escape_options(player_color)
    assert sorted(escape_options) == sorted(expected_value),f"\033[91mreturned:{escape_options}\033[m \033[92mexpected:{expected_value}\033[m"
    print(emojize("Passed :check_mark:"))
    



json_file_3 = open('tests\\test_set_check_escape.json','r')
test_set_3 = json.load(json_file_3)

print("testing player in check function")
for test in test_set_3:
    print(f"\033[93m{test}\033[m")
    test = test_set_3[test]
    test_check_escape(test["board"],test["player"],test["expected_value"])
    
"""    
json_file = open('tests\test_set_predict.json','r')
predict_function_test_set = json.load(json_file)
print("testing predict function")
for test in predict_function_test_set:
    print(f"\033[93m{test}\033[m")
    test = predict_function_test_set[test]
    test_predict_function(test["board"],test["piece_color"],test["piece_type"],test["piece_position"],test["expected_value"])

json_file_2 = open('tests\test_set_player_in_check.json','r')
player_in_check_test_set = json.load(json_file_2)

print("testing player in check function")
for test in player_in_check_test_set:
    print(f"\033[93m{test}\033[m")
    test = player_in_check_test_set[test]
    test_check_function(test["board"],test["player"],test["expected_value"])
"""