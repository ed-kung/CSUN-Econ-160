"""
Build the data files for the online Random Problem Generator (rpg.md / rpg.py).

A problem class takes part by declaring a topic (one dropdown entry):

    class RevealedPreference(GenericProblem):
        rpg_topic = "revealed-preference"     # slug -> assets/data/<slug>-practice.json
        rpg_title = "Revealed Preference"     # dropdown label (default: from the slug)
        rpg_order = 10                        # dropdown position (optional, low first)
        rpg_samples = 20                      # problems sampled into the JSON (optional)

To control the mix of cases within a class, declare target shares and a labeler:

        rpg_mix = {"corner": 0.3, "interior": 0.7}   # shares (normalized if they don't sum to 1)

        @staticmethod                                 # or @classmethod
        def rpg_stratum(row):                         # row: one valid-params pd.Series
            return "corner" if row["x"] == 0 else "interior"

rpg_samples is then split across the labels by largest remainder (so the counts
sum exactly to rpg_samples). Rows whose label isn't in rpg_mix are never drawn. If
a label has too few valid rows, it gets them all and a warning is printed; the
shortfall is not filled from other labels, so the mix stays close to the target.

Several classes may share a topic; their samples are pooled. A class can override
how a problem is shown online by defining `rpg_entries(self)`, returning a list of
{"setup": html, "solution": html} dicts (default: formats.get_online_format(self)).
The online strings are written to the JSON as-is: each problem is responsible for
providing properly formatted online (HTML/MathJax) setups and answers.

build_rpg() rebuilds everything from the saved valid-params files:
  - assets/data/<slug>-practice.json   one per topic
  - _data/rpg_topics.yml               the dropdown options, read by rpg.md
  - rpg.toml [files]                   so pyscript fetches each JSON
Sampling is seeded by each class's `seed`, so unchanged problems give unchanged files.
"""

import glob
import json
import os
import tomllib

import numpy as np
import pandas as pd

from econtools.problems import formats
from econtools.problems import generate as _generate

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DATA_DIR = os.path.join(REPO_DIR, "assets", "data")
TOPICS_YML = os.path.join(REPO_DIR, "_data", "rpg_topics.yml")
RPG_TOML = os.path.join(REPO_DIR, "rpg.toml")
URL_PREFIX = "/CSUN-Econ-160/assets/data"

DEFAULT_SAMPLES = 20
DEFAULT_ORDER = 1000


def _json_filename(slug):
    return f"{slug}-practice.json"


def _title_from_slug(slug):
    return slug.replace("-", " ").replace("_", " ").title()


def collect_topics(registry):
    """{slug: {"title", "order", "classes"}} for every class with an rpg_topic."""
    topics = {}
    for name in registry.names():
        cls = registry[name]
        slug = getattr(cls, "rpg_topic", None)
        if not slug:
            continue
        t = topics.setdefault(slug, {"title": None, "order": DEFAULT_ORDER, "classes": []})
        t["classes"].append(cls)
        t["title"] = t["title"] or getattr(cls, "rpg_title", None)
        t["order"] = min(t["order"], getattr(cls, "rpg_order", DEFAULT_ORDER))
    for slug, t in topics.items():
        t["title"] = t["title"] or _title_from_slug(slug)
    return dict(sorted(topics.items(), key=lambda kv: (kv[1]["order"], kv[1]["title"])))


def _allocate(n, mix):
    """Split n into integer counts per label proportional to mix (largest remainder)."""
    total = sum(mix.values())
    if total <= 0:
        raise ValueError(f"rpg_mix shares must sum to a positive number, got {mix}")
    exact = {k: n * v / total for k, v in mix.items()}
    counts = {k: int(np.floor(x)) for k, x in exact.items()}
    leftover = n - sum(counts.values())
    # Ties broken by declaration order, so the allocation is deterministic
    by_remainder = sorted(exact, key=lambda k: exact[k] - counts[k], reverse=True)
    for k in by_remainder[:leftover]:
        counts[k] += 1
    return counts


def _sample_rows(cls, df, rng):
    """Pick the rows to show: uniform, or stratified by cls.rpg_mix if declared."""
    n_target = getattr(cls, "rpg_samples", DEFAULT_SAMPLES)
    mix = getattr(cls, "rpg_mix", None)
    if not mix:
        return df.sample(n=min(n_target, len(df)), random_state=rng)

    if not hasattr(cls, "rpg_stratum"):
        raise AttributeError(f"{cls.__name__} sets rpg_mix but does not define rpg_stratum(row)")
    labels = df.apply(cls.rpg_stratum, axis=1)
    unknown = set(labels) - set(mix)
    if unknown:
        print(f"RPG: {cls.__name__}: labels {sorted(map(str, unknown))} not in rpg_mix; those rows are skipped")

    parts = []
    for label, want in _allocate(n_target, mix).items():
        pool = df[labels == label]
        k = min(want, len(pool))
        if k < want:
            print(f"RPG: {cls.__name__}: wanted {want} '{label}' problems, only {len(pool)} valid")
        if k:
            parts.append(pool.sample(n=k, random_state=rng))
    if not parts:
        return df.iloc[0:0]
    # Shuffle so the strata are interleaved in the output
    return pd.concat(parts).sample(frac=1, random_state=rng)


def sample_entries(cls, data_dir=None):
    """Sample up to cls.rpg_samples valid problems and render them for the web."""
    df = _generate.load_valid(cls, data_dir)
    rng = np.random.default_rng(cls.seed)
    rows = _sample_rows(cls, df, rng)
    entries = []
    for i, (_, row) in enumerate(rows.iterrows()):
        prob = cls(params=row.to_dict(), rng=rng, name=f"{cls._default_instance_name()}_rpg{i}")
        if hasattr(prob, "rpg_entries"):
            new = prob.rpg_entries()
        else:
            new = [formats.get_online_format(prob)]
        entries.extend(new)
    return entries


def _write_topics_yml(topics):
    os.makedirs(os.path.dirname(TOPICS_YML), exist_ok=True)
    lines = ["# Generated by `python -m problems`; do not edit by hand."]
    for slug, t in topics.items():
        # JSON strings are valid YAML double-quoted scalars
        lines.append(f"- slug: {json.dumps(slug)}")
        lines.append(f"  title: {json.dumps(t['title'])}")
    with open(TOPICS_YML, "w") as f:
        f.write("\n".join(lines) + "\n")


def _write_rpg_toml(slugs):
    with open(RPG_TOML, "rb") as f:
        cfg = tomllib.load(f)
    lines = []
    for key, val in cfg.items():
        if key != "files":
            lines.append(f"{key} = {json.dumps(val)}")
    lines.append("")
    lines.append("# [files] is generated by `python -m problems`; edit the rest freely.")
    lines.append("[files]")
    for slug in slugs:
        lines.append(f"{json.dumps(URL_PREFIX + '/' + _json_filename(slug))} = \"\"")
    with open(RPG_TOML, "w") as f:
        f.write("\n".join(lines) + "\n")


def build_rpg(registry, data_dir=None, verbose=True):
    """Rebuild every RPG topic file, the dropdown list, and rpg.toml. Returns {slug: count}."""
    os.makedirs(ASSETS_DATA_DIR, exist_ok=True)
    topics = collect_topics(registry)
    written = {}
    for slug, t in topics.items():
        entries = []
        for cls in t["classes"]:
            try:
                entries.extend(sample_entries(cls, data_dir))
            except FileNotFoundError as e:
                print(f"RPG: skipping {cls.__name__} ({e})")
        if not entries:
            continue
        path = os.path.join(ASSETS_DATA_DIR, _json_filename(slug))
        with open(path, "w") as f:
            json.dump(entries, f, indent=2)
            f.write("\n")
        written[slug] = len(entries)
        if verbose:
            print(f"RPG: {slug}: {len(entries)} problems -> {path}")

    # Remove practice files for topics that no longer exist
    keep = {_json_filename(s) for s in written}
    for path in glob.glob(os.path.join(ASSETS_DATA_DIR, "*-practice.json")):
        if os.path.basename(path) not in keep:
            os.remove(path)
            if verbose:
                print(f"RPG: removed stale {path}")

    _write_topics_yml({s: t for s, t in topics.items() if s in written})
    _write_rpg_toml(list(written))
    return written
