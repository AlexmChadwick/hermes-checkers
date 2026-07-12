from checkers.board import Board, Piece, Player, Square
from checkers.game import Game, GameStatus
from checkers.moves import Move, all_legal_moves, apply_move


def test_initial_board_has_twelve_pieces_each():
    board = Board()
    assert board.count_for(Player.RED) == 12
    assert board.count_for(Player.BLACK) == 12


def test_simple_move_for_red():
    board = Board.from_rows(
        [
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . r . . .",
        ]
    )
    start = Square(7, 4)
    moves = all_legal_moves(board, Player.RED)
    assert Move((start, Square(6, 3))) in moves


def test_must_capture_when_available():
    board = Board.from_rows(
        [
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . b . . . .",
            ". . r . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
        ]
    )
    moves = all_legal_moves(board, Player.RED)
    assert moves
    assert all(abs(m.start.row - m.end.row) >= 2 for m in moves)
    apply_move(board, moves[0], Player.RED)
    assert board.piece_at(Square(4, 3)) is Piece.EMPTY
    assert board.piece_at(Square(3, 4)) is Piece.RED


def test_promotion_to_king():
    board = Board.from_rows(
        [
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . R . . .",
        ]
    )
    move = Move((Square(7, 4), Square(6, 3)))
    apply_move(board, move, Player.RED)
    assert board.piece_at(Square(6, 3)) is Piece.RED_KING


def test_game_detects_win_by_capture():
    game = Game(Board.from_rows(
        [
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . . . . .",
            ". . . . r . . .",
        ]
    ))
    game.turn = Player.BLACK
    assert game.status() is GameStatus.RED_WINS