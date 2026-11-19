"""
python -m problems [names...] [--data-dir DIR] [--dry-run] [--with-deps] [--list]

Generates the valid-params parquet file for each requested problem type, then
rebuilds the Random Problem Generator files (see problems/_rpg.py).
"""

import argparse
import sys

from econtools.problems.generate import main

from problems import REGISTRY
from problems._rpg import build_rpg

main(REGISTRY)

# main() has already validated the arguments; pick out the ones the RPG step needs.
_pre = argparse.ArgumentParser(add_help=False)
_pre.add_argument("--data-dir", default=None)
_pre.add_argument("--dry-run", action="store_true")
_pre.add_argument("--list", action="store_true")
_args, _ = _pre.parse_known_args(sys.argv[1:])

if not (_args.dry_run or _args.list):
    build_rpg(REGISTRY, data_dir=_args.data_dir)
