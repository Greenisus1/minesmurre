# Minesmurre

An offline terminal mines puzzle. Reveal all safe squares without hitting a mine. Numbers count mines in the eight neighboring squares. Zero areas flood open. Flags are your notes, not proof that a square is mined.

Python 3.9+, standard library only. No network, packages, timer, accounts, purchases or saved records.

## Start

Download this private repo ZIP while signed into GitHub, extract it and open a terminal inside the folder.

```text
python3 minesmurre.py
python3 minesmurre.py --size 6 --mines 6
python3 minesmurre.py --seed 42
python3 minesmurre.py --demo --seed 42
python3 -m unittest -v
bash app-store.sh install
bash app-store.sh run
```

Default: 8 by 8 with 10 mines. Size 4-12. Mines range from 1 to `size * size - 9`, leaving enough room to protect the first revealed square and all its neighbors. Mines are placed only on the first successful reveal. Flags placed before that do not place mines. The first reveal is guaranteed zero and its adjacent squares are safe. Later moves may require guessing; this is **not** a no-guess puzzle generator.

Commands use 1-based row/column numbers, followed by Enter:

```text
R 1 1
F 3 4
Q
```

R reveals. F toggles a flag. Remove a flag before revealing that square. Flags are capped at the mine count, and revealed squares cannot be flagged. A flood skips flags, even if they are wrong; unflag and reveal those safe squares to finish. Repeating an already revealed square costs no action. Invalid commands do not count an action.

Winning requires all safe squares revealed, not all mines flagged. Hitting a mine ends the round and shows all mines. Quitting does not reveal the layout or write any file. To play again, run the app again. Seeded boards are repeatable only for the same first reveal and generator; a different starting square changes placement. No leaderboards or claims of secure randomness.

The public-only Pi App Store cannot fetch this private repository. Root marker/version files are staged for later publication or authenticated support.

16 tests cover 50 safe-first boards, mine counts, flags, flood/repeat behavior, win/loss, bounds, deterministic starts and CLI. Linux tested, physical Pi/non-Linux platforms untested. Original ASCII implementation, no copied assets.
