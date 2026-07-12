from __future__ import annotations

import argparse
import sys

from checkers.board import Square
from checkers.game import Game, GameStatus
from checkers.moves import Move


def _parse_square(token: str) -> Square:
    token = token.strip().lower()
    if len(token) != 2 or not token[0].isdigit() or not token[1].isdigit():
        raise ValueError(f"invalid square {token!r}, use rowcol like 52")
    row, col = int(token[0]), int(token[1])
    return Square(row, col)


def _format_move(move: Move) -> str:
    parts = [f"{sq.row}{sq.col}" for sq in move.path]
    return "->".join(parts)


def _prompt_move(game: Game) -> Move:
    legal = game.legal_moves()
    print(game.board.render())
    print(f"{game.turn.value} to move ({len(legal)} legal)")
    while True:
        raw = input("move (e.g. 52->43 or q): ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            raise SystemExit(0)
        try:
            if "->" not in raw:
                raise ValueError("use start->end or multi-jump with ->")
            squares = [_parse_square(part) for part in raw.split("->")]
            candidate = Move(tuple(squares))
            if candidate not in legal:
                print("illegal move; try again")
                continue
            return candidate
        except ValueError as exc:
            print(exc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Play American checkers in the terminal")
    parser.add_argument(
        "--list-moves",
        action="store_true",
        help="print legal moves for the current player and exit",
    )
    args = parser.parse_args(argv)

    game = Game.new()
    while True:
        status = game.status()
        if status is not GameStatus.IN_PROGRESS:
            print(game.board.render())
            print(status.value.replace("_", " "))
            return 0

        if args.list_moves:
            for move in game.legal_moves():
                print(_format_move(move))
            return 0

        move = _prompt_move(game)
        game.apply(move)

    return 0


if __name__ == "__main__":
    sys.exit(main())