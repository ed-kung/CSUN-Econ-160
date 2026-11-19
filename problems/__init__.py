"""
Auto-generated problems for Econ 160, built on econtools.problems.

Each module in this package defines one or more GenericProblem subclasses;
discover() registers them all in REGISTRY. Generate valid parameter files with:

    python -m problems [ProblemName ...]
"""

import os

from econtools.problems.base import config
from econtools.problems.registry import Registry, discover

_HERE = os.path.dirname(os.path.abspath(__file__))
config.data_dir = os.path.join(_HERE, "data")
config.image_dir = os.path.join(_HERE, "..", "assets", "images", "graphs")
config.image_url_prefix = "/CSUN-Econ-160/assets/images/graphs"

REGISTRY = Registry()
discover(__name__, REGISTRY)
