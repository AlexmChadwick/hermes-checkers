from __future__ import annotations

from dataclasses import dataclass

from checkers.board import Board, Piece, Player, Square


@dataclass(frozen=True)
class Move:
    path: tuple[Square, ...]

    @property
    def start(self) -> Square:
        return self.path[0]

    @property
    def end(self) -> Square:
        return self.path[-1]

    def jumps(self) -> list[tuple[Square, Square]]:
        pairs: list[tuple[Square, Square]] = []
        for i in range(len(self.path) - 1):
            a, b = self.path[i], self.path[i + 1]
            if abs(a.row - b.row) == 2:
                pairs.append((a, b))
        return pairs


def _directions(piece: Piece) -> list[tuple[int, int]]:
    if piece.is_king():
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if piece is Piece.RED:
        return [(-1, -1), (-1, 1)]
    return [(1, -1), (1, 1)]


def _slide(board: Board, start: Square, dr: int, dc: int) -> Square | None:
    row, col = start.row + dr, start.col + dc
    while 0 <= row < Board.SIZE and 0 <= col < Board.SIZE:
        sq = Square(row, col)
        if not sq.is_dark():
            return None
        if board.piece_at(sq) is not Piece.EMPTY:
            return sq
        row += dr
        col += dc
    return None


def _simple_moves(board: Board, start: Square, piece: Piece, player: Player) -> list[Move]:
    moves: list[Move] = []
    for dr, dc in _directions(piece):
        row, col = start.row + dr, start.col + dc
        if 0 <= row < Board.SIZE and 0 <= col < Board.SIZE:
            dest = Square(row, col)
            if dest.is_dark() and board.piece_at(dest) is Piece.EMPTY:
                moves.append(Move((start, dest)))
    return moves


def _capture_chains(
    board: Board,
    start: Square,
    piece: Piece,
    player: Player,
    visited: frozenset[Square],
) -> list[Move]:
    chains: list[Move] = []
    for dr, dc in _directions(piece):
        mid_row, mid_col = start.row + dr, start.col + dc
        land_row, land_col = start.row + 2 * dr, start.col + 2 * dc
        if not (0 <= land_row < Board.SIZE and 0 <= land_col < Board.SIZE):
            continue
        mid = Square(mid_row, mid_col)
        land = Square(land_row, land_col)
        if not mid.is_dark() or not land.is_dark():
            continue
        mid_piece = board.piece_at(mid)
        if mid_piece is Piece.EMPTY or mid_piece.owner() == player:
            continue
        if board.piece_at(land) is not Piece.EMPTY:
            continue

        temp = board.copy()
        temp.set_piece(start, Piece.EMPTY)
        temp.set_piece(mid, Piece.EMPTY)
        temp.set_piece(land, piece)
        further = _capture_chains(temp, land, piece, player, visited | {mid})
        if further:
            for sub in further:
                chains.append(Move((start, *sub.path[1:])))
        else:
            chains.append(Move((start, land)))
    return chains


def legal_moves(board: Board, player: Player, start: Square) -> list[Move]:
    piece = board.piece_at(start)
    if piece.owner() != player:
        return []

    captures: list[Move] = []
    for sq, p in board.pieces_for(player):
        captures.extend(_capture_chains(board, sq, p, player, frozenset()))

    if captures:
        return [m for m in captures if m.start == start]

    return _simple_moves(board, start, piece, player)


def all_legal_moves(board: Board, player: Player) -> list[Move]:
    captures: list[Move] = []
    for sq, piece in board.pieces_for(player):
        captures.extend(_capture_chains(board, sq, piece, player, frozenset()))
    if captures:
        return captures

    moves: list[Move] = []
    for sq, piece in board.pieces_for(player):
        moves.extend(_simple_moves(board, sq, piece, player))
    return moves


def apply_move(board: Board, move: Move, player: Player) -> None:
    piece = board.piece_at(move.start)
    if piece.owner() != player:
        raise ValueError("wrong player for move")

    board.set_piece(move.start, Piece.EMPTY)
    for from_sq, over_sq in move.jumps():
        mid = Square(
            (from_sq.row + over_sq.row) // 2,
            (from_sq.col + over_sq.col) // 2,
        )
        board.set_piece(mid, Piece.EMPTY)

    promoted = _maybe_promote(piece, move.end, player)
    board.set_piece(move.end, promoted)


def _maybe_promote(piece: Piece, dest: Square, player: Player) -> Piece:
    if piece.is_king():
        return piece
    if player is Player.RED and dest.row == 0:
        return Piece.RED_KING
    if player is Player.BLACK and dest.row == 7:
        return Piece.BLACK_KING
    return piece