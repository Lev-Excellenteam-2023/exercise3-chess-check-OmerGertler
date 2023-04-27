import pytest
from unittest.mock import Mock
import Piece
from enums import Player
import ai_engine
import chess_engine


# unit tests

def test_get_valid_piece_takes_everything_is_free_around():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Player.EMPTY
    mock_game_state.is_valid_piece = lambda row, col: False

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 0

    expected_moves = []
    for move in expected_moves:
        assert move in valid_moves

    invalid_moves = [(2, 2), (2, 4), (3, 3), (3, 5), (5, 3), (5, 5), (6, 4), (6, 6)]
    for move in invalid_moves:
        assert move not in valid_moves


def test_get_valid_piece_takes_cant_take_at_all():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)
    mock_game_state.is_valid_piece = lambda row, col: True

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 0

    expected_moves = []
    for move in expected_moves:
        assert move in valid_moves

    invalid_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in invalid_moves:
        assert move not in valid_moves


def test_get_valid_piece_takes_can_take_all():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)
    mock_game_state.is_valid_piece = lambda row, col: True

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 8

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in valid_moves

    invalid_moves = [(2, 2), (2, 4), (3, 3), (3, 5), (5, 3), (5, 5), (6, 4), (6, 6)]
    for move in invalid_moves:
        assert move not in valid_moves


def test_get_valid_peaceful_moves_everything_is_free_around():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Player.EMPTY

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 8

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in valid_moves

    invalid_moves = [(2, 2), (2, 4), (3, 3), (3, 5), (5, 3), (5, 5), (6, 4), (6, 6)]
    for move in invalid_moves:
        assert move not in valid_moves


def test_get_valid_peaceful_moves_opponent_surrounding():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 0

    expected_moves = []
    for move in expected_moves:
        assert move in valid_moves

    invalid_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in invalid_moves:
        assert move not in valid_moves


def test_get_valid_peaceful_moves_self_surrounding():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 0

    expected_moves = []
    for move in expected_moves:
        assert move in valid_moves

    invalid_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in invalid_moves:
        assert move not in valid_moves


# integration tests

def test_get_valid_piece_moves():
    mock_game_state = Mock()
    mock_game_state.get_valid_piece_takes = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    mock_game_state.get_valid_peaceful_moves = []
    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    all_moves = Piece.Knight.get_valid_piece_moves(mock_self_knight, mock_game_state)

    assert len(all_moves) == 8

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in all_moves


def test_evaluate_board():
    mock_game_state = Mock()
    mock_self_ai = Mock()

    mock_game_state.is_valid_piece = lambda row, col: True
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)
    mock_self_ai.get_piece_value = lambda evaluated_piece, player: 50

    expected_evaluation_score = 50*8*8
    evaluation_score = ai_engine.chess_ai.evaluate_board(mock_self_ai, mock_game_state, Player.PLAYER_1)
    assert expected_evaluation_score == evaluation_score


# system test

def test_move_piece():
    game = chess_engine.game_state()
    game.move_piece((1, 2), (2, 2), False)
    game.move_piece((6, 3), (4, 3), False)
    game.move_piece((1, 1), (3, 1), False)
    game.move_piece((7, 4), (3, 0), False)
    assert game.checkmate_stalemate_checker() == 0

