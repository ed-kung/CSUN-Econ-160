"""
Auto-generated problems for Econ 160, built on econtools.problems.

Each module in this package defines one or more GenericProblem subclasses;
discover() registers them all in REGISTRY. Generate valid parameter files with:

    python -m problems [ProblemName ...]
"""

import os

import matplotlib as mpl
from econtools.problems.base import config
from econtools.problems.registry import Registry, discover

_HERE = os.path.dirname(os.path.abspath(__file__))
config.data_dir = os.path.join(_HERE, "data")
config.image_dir = os.path.join(_HERE, "..", "assets", "images", "graphs")
config.image_url_prefix = "/CSUN-Econ-160/assets/images/graphs"

# Course-wide matplotlib defaults for problem graphs: square, ~3in printed
# (matches config.latex_image_width), 11pt text.
mpl.rcParams.update({
    "figure.figsize": (3.5, 3.5),
    "font.size": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "savefig.dpi": 200,     # 600px PNGs: crisp in print, reasonable on the web
})

REGISTRY = Registry()
discover(__name__, REGISTRY)
