"""
Test script: build a sample PDF exam that covers every problem type in the
course's problems package.

For each type registered in problems.REGISTRY, a valid problem is sampled from
problems/data/<ClassName>.parquet (via REGISTRY.sample_problem), rendered with
econtools.problems.formats, and added to an econtools.assignments.latex.Exam
as a multipart multiple-choice question. The exam is multiple choice only.

An exam PDF and a solutions PDF are compiled into tests/output/.

Run from the repo root (generate the data files first if they don't exist):
    export PYTHONPATH=$HOME/projects/econtools/src
    .venv/bin/python -m problems
    .venv/bin/python tests/test_sample_exam.py
"""

import os
import shutil
import sys

import numpy as np

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(TESTS_DIR)
OUTPUT_DIR = os.path.join(TESTS_DIR, "output")

# Make `problems` (this repo) and `econtools` (sibling checkout) importable
# no matter where the script is run from.
sys.path.insert(0, REPO_DIR)
sys.path.insert(0, os.path.expanduser("~/projects/econtools/src"))

from econtools.assignments.latex import Exam  # noqa: E402
from econtools.problems import formats  # noqa: E402
from econtools.problems import generate  # noqa: E402
from problems import REGISTRY  # noqa: E402


def problem_types():
    """Every registered problem type; fails if any is missing its valid-params file."""
    names = REGISTRY.names()
    assert names, "no problem types registered in problems/"
    missing = [n for n in names if not os.path.exists(generate.data_path(REGISTRY[n]))]
    assert not missing, (
        f"no valid-params data for {missing}; run `.venv/bin/python -m problems` first")
    return names


def build_exam(rng, names):
    """One multipart MCQ per problem type. Returns (exam, number of MCQs, problems)."""
    exam = Exam("ECON 160 Sample Exam", version="A", time=30)

    n_mcq = 0
    probs = []
    for name in names:
        prob = REGISTRY.sample_problem(name, rng=rng, name=name)
        # only the questions that have a multiple-choice form
        qids = [i for i, q in enumerate(prob.question_list) if q["MCQ"] is not None]
        assert qids, f"{name} has no multiple-choice questions"
        exam.add(formats.get_multipart_mcq(prob, question_ids=qids))
        n_mcq += len(qids)
        probs.append(prob)

    return exam, n_mcq, probs


def main():
    names = problem_types()
    print(f"Problem types: {', '.join(names)}")

    exam, n_mcq, probs = build_exam(np.random.default_rng(0), names)

    tex = exam.texify()
    sol_tex = exam.texify(solutions=True)
    assert "Answer:" not in tex
    assert sol_tex.count("Answer:") == n_mcq, (sol_tex.count("Answer:"), n_mcq)
    for prob in probs:
        assert prob.setup_list[0]["setup"] in tex

    # Reproducibility: same seed -> same exam
    exam2, _, _ = build_exam(np.random.default_rng(0), names)
    assert exam2.texify(solutions=True) == sol_tex

    if shutil.which("pdflatex") is None:
        print("pdflatex not found; skipping PDF compilation")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name, solutions in (("sample_exam", False), ("sample_exam_solutions", True)):
        pdf = os.path.join(OUTPUT_DIR, f"{name}.pdf")
        if os.path.exists(pdf):
            os.remove(pdf)
        exam.print_pdf(name, OUTPUT_DIR, solutions=solutions)
        assert os.path.exists(pdf), f"{pdf} was not produced"
        print(f"Wrote {pdf}")

    print("All checks passed.")


if __name__ == "__main__":
    main()
