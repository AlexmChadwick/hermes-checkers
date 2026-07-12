from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Player(Enum):
    RED = "red"
    BLACK = "black"

    def opponent(self) -> Player:
        return Player.BLACK if self is Player.RED else Player.RED


class Piece(Enum):
    EMPTY = "."
    RED = "r"
    RED_KING = "R"
    BLACK = "b"
    BLACK_KING = "B"

    def owner(self) -> Player | None:
        if self in (Piece.RED, Piece.RED_KING):
            return Player.RED
        if self in (Piece.BLACK, Piece.BLACK_KING):
            return Player.BLACK
        return None

    def is_king(self) -> bool:
        return self in (Piece.RED_KING, Piece.BLACK_KING)


@dataclass(frozen=True)
class Square:
    row: int
    col: int

    def is_dark(self) -> bool:
        return (self.row + self.col) % 2 == 1

    def in_bounds(self) -> bool:
        return 0 <= self.row < 8 and 0 <= self.col < 8


class Board:
    SIZE = 8

    def __init__(self, squares: list[list[Piece]] | None = None) -> None:
        if squares is None:
            self._squares = self._initial_squares()
        else:
            self._squares = squares

    @staticmethod
    def _initial_squares() -> list[list[Piece]]:
        grid = [[Piece.EMPTY for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        for row in range(3):
            for col in range(Board.SIZE):
                if (row + col) % 2 == 1:
                    grid[row][col] = Piece.BLACK
        for row in range(5, 8):
            for col in range(Board.SIZE):
                if (row + col) % 2 == 1:
                    grid[row][col] = Piece.RED
        return grid

    def copy(self) -> Board:
        return Board([row[:] for row in self._squares])

    def piece_at(self, square: Square) -> Piece:
        return self._squares[square.row][square.col]

    def set_piece(self, square: Square, piece: Piece) -> None:
        self._squares[square.row][square.col] = piece

    def pieces_for(self, player: Player) -> list[tuple[Square, Piece]]:
        out: list[tuple[Square, Piece]] = []
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                sq = Square(row, col)
                piece = self.piece_at(sq)
                if piece.owner() == player:
                    out.append((sq, piece))
        return out

    def count_for(self, player: Player) -> int:
        return sum(1 for _, p in self.pieces_for(player))

    def render(self) -> str:
        lines = ["  " + " ".join(str(c) for c in range(Board.SIZE))]
        for row in range(Board.SIZE):
            cells = [self._squares[row][col].value for col in range(Board.SIZE)]
            lines.append(f"{row} " + " ".join(cells))
        return "\n".join(lines)

    @classmethod
    def from_rows(cls, rows: Iterable[str]) -> Board:
        grid: list[list[Piece]] = []
        for line in rows:
            tokens = line.strip().split()
            if len(tokens) != Board.SIZE:
                raise ValueError(f"expected {Board.SIZE} cells, got {len(tokens)}")
            grid.append([Piece(t) for t in tokens])
        if len(grid) != Board.SIZE:
            raise ValueError(f"expected {Board.SIZE} rows")
        return Board(grid)