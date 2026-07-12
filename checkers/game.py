from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from checkers.board import Board, Player
from checkers.moves import Move, all_legal_moves, apply_move


class GameStatus(Enum):
    IN_PROGRESS = "in_progress"
    RED_WINS = "red_wins"
    BLACK_WINS = "black_wins"
    DRAW = "draw"


@dataclass
class Game:
    board: Board
    turn: Player = Player.RED

    @classmethod
    def new(cls) -> Game:
        return Game(Board())

    def legal_moves(self) -> list[Move]:
        return all_legal_moves(self.board, self.turn)

    def apply(self, move: Move) -> None:
        legal = self.legal_moves()
        if move not in legal:
            raise ValueError("illegal move")
        apply_move(self.board, move, self.turn)
        self.turn = self.turn.opponent()

    def status(self) -> GameStatus:
        red_count = self.board.count_for(Player.RED)
        black_count = self.board.count_for(Player.BLACK)
        if red_count == 0:
            return GameStatus.BLACK_WINS
        if black_count == 0:
            return GameStatus.RED_WINS
        if not all_legal_moves(self.board, self.turn):
            return (
                GameStatus.BLACK_WINS
                if self.turn is Player.RED
                else GameStatus.RED_WINS
            )
        return GameStatus.IN_PROGRESS