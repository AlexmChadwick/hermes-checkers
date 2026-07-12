# hermes-checkers

Playable **American checkers** (8×8 draughts) built as a Hermes **coder** profile demo: small Python package, tests, and a terminal UI for two players on one keyboard.

## Features

- Standard 8×8 board with pieces on dark squares only
- Mandatory captures and multi-jump chains
- King promotion on the far rank
- Win when the opponent has no pieces or no legal moves

## Quick start

```bash
cd hermes-checkers
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m checkers.cli
```

### Move notation

Enter moves as square coordinates `rowcol` joined with `->`, for example:

- `52->43` — simple move
- `52->34->26` — double jump

Coordinates match the printed board (`0`–`7` on both axes). Type `q` to quit.

List legal moves for the current position without playing:

```bash
python -m checkers.cli --list-moves
```

## Layout

| Path | Purpose |
|------|---------|
| `checkers/board.py` | Board state and rendering |
| `checkers/moves.py` | Legal move generation and application |
| `checkers/game.py` | Turn order and win detection |
| `checkers/cli.py` | Interactive terminal game |
| `tests/` | Pytest coverage for moves and outcomes |

## License

MIT — use and hack freely.