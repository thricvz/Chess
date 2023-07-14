from modules import Board
import json
from emoji import emojize

def test_predict_function(test_set_file="test_sets\\predict_moves.json"):
    test_set = open(test_set_file,'r')
    test_set = json.load(test_set)
    for test in test_set:
        test_number = test
        test = test_set[test]
        board =  Board()
        board.build_from_text(test["board"])
        for piece in board.pieces_in_play:
            if piece.type == test["piece_type"] and piece.color == test["piece_color"] and piece.position == test["piece_position"]:
                selected_piece = piece

        selected_piece.possible_moves = board.predict_moves(selected_piece)
        return_value = selected_piece.possible_moves
        expected_value = test["expected_value"]
        assert sorted(return_value) == sorted(expected_value),f"\033[95m{test_number}:\033[m \033[91mreturned:{return_value}\033[m \033[92mexpected:{expected_value}\033[m"

def test_check_function(test_set_file="test_sets\\player_in_check.json"):
    test_set = open(test_set_file,'r')
    test_set = json.load(test_set)
    for test in test_set:
        test_number = test
        test = test_set[test]
        board = Board()
        board.build_from_text(test["board"])
        board.update_pieces_statuses()
        return_value = board.player_in_check(test["player"])
        expected_value = test["expected_value"]
        assert str(return_value) == expected_value,f"\033[95m{test_number}:\033[m \033[91mreturned:{return_value}\033[m \033[92mexpected:{expected_value}\033[m"
        

def test_check_escape(test_set_file="test_sets\\check_escape.json"):
    test_set = open(test_set_file,'r')
    test_set = json.load(test_set)
    for test in test_set:
        test_number = test
        test = test_set[test]
        board = Board()
        board.build_from_text(test["board"])
        board.update_pieces_statuses()
        return_value = board.check_escape_options(test["player"])
        expected_value = test["expected_value"]
        assert sorted(return_value) == sorted(expected_value),f"\033[95m{test_number}:\033[m \033[91mreturned:{return_value}\033[m \033[92mexpected:{expected_value}\033[m"
    
def test_checkmate(test_set_file="test_sets\\checkmate.json"):
    test_set = open(test_set_file,'r')
    test_set = json.load(test_set)
    for test in test_set:
        test_number = test
        test = test_set[test]
        board = Board()
        board.build_from_text(test["board"])
        board.update_pieces_statuses()
        return_value = board.checkmate(test["player"])
        expected_value = test["expected_value"]
        assert str(return_value) == expected_value,f"\033[95m{test_number}:\033[m \033[91mreturned:{return_value}\033[m \033[92mexpected:{expected_value}\033[m"

def test_stalemate(test_set_file ="test_sets\\stalemate.json"):
    test_set = open(test_set_file,'r')
    test_set = json.load(test_set)
    for test in test_set:
        test_number = test
        test = test_set[test]
        board = Board()
        board.build_from_text(test["board"])
        board.update_pieces_statuses()
        return_value = board.stalemate(test["player"])
        expected_value = test["expected_value"]
        assert str(return_value) == expected_value,f"\033[95m{test_number}:\033[m \033[91mreturned:{return_value}\033[m \033[92mexpected:{expected_value}\033[m"

def test_castle_options(test_set_file="test_sets\\castle_options.json"):
    test_set = open(test_set_file,'r')
    test_set = json.load(test_set)
    for test in test_set:
        test_number = test
        test = test_set[test]
        board = Board()
        board.build_from_text(test["board"])
        board.update_pieces_statuses()
        return_value = board.castle_options(test["player"])
        expected_value = test["expected_value"]
        assert return_value == expected_value,f"\033[95m{test_number}:\033[m \033[91mreturned:{return_value}\033[m \033[92mexpected:{expected_value}\033[m"

