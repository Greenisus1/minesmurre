# Minesmurre

Offline terminal mines puzzle, with a cursor-driven colored board. Reveal every safe square to win; flags mark suspected mines but do not guarantee correctness. The first reveal and its neighbors are safe. Flood reveal opens connected zeros. Some boards need guesses; no claim of a no-guess solver.

## Run

    bash app-store.sh install
    bash app-store.sh run

Python3 and its standard-library curses (normally included on Linux). No desktop, account or network needed after download. Arrows/WASD move, Space/Enter reveals, F toggles flag, R restarts, Q quits. Resize needs at least 56 columns and board size+10 rows. Smaller windows display a resize notice and keep the board. Type `python3 minesmurre.py --plain` for coordinate commands, or `--demo` for a seeded/sample display. Plain mode also selected automatically without a usable TTY.

    python3 minesmurre.py --size 10 --mines 18
    python3 minesmurre.py --seed 42 --demo

Boards 4-12 across; flags capped at mine count, opened squares cannot be flagged. Seed restarts the same board if chosen. No saves, undo, hints, sound or GUI. No assets from another game.

## Tests and limits

    python3 -m unittest -v test_minesmurre.py

Core 16 tests plus terminal/pixel and input-flow smoke on Linux. Version 1.1.0 adds curses presentation and games category while keeping existing core rules. Linux tested; physical Raspberry Pi and non-Linux untested. curses may not be installed on non-Linux; use --plain. Terminal app only; no desktop required.
