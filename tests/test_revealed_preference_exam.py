"""
Test script: build a sample PDF exam from the course's problems package.

Samples RevealedPreference problems from problems/data/RevealedPreference.parquet
(via REGISTRY.sample_problem), renders them with econtools.problems.formats,
assembles them into an econtools.assignments.latex.Exam, and compiles an exam
PDF plus a solutions PDF into tests/output/.

Run from the repo root (generate the data file first if it doesn't exist):
    export PYTHONPATH=$HOME/projects/econtools/src
    .venv/bin/python -m problems RevealedPreference
    .venv/bin/python tests/test_revealed_preference_exam.py
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

from econtools.assignments.latex import Exam, RawLatex  # noqa: E402
from econtools.problems import formats  # noqa: E402
from problems import REGISTRY  # noqa: E402


def build_exam(rng):
    exam = Exam("ECON 160 Sample Exam", version="A", time=30)

    exam.add(RawLatex("\\noindent\\textbf{Part I: Multiple choice}\n"))

    # 1. Multipart MCQ: one setup, every question as a multiple-choice part
    prob = REGISTRY.sample_problem("RevealedPreference", rng=rng, name="rp1")
    exam.add(formats.get_multipart_mcq(prob))

    # 2-3. Single MCQs: setup prepended to one chosen question
    for i, qid in enumerate((0, 1), start=2):
        prob = REGISTRY.sample_problem("RevealedPreference", rng=rng, name=f"rp{i}")
        exam.add(formats.get_single_mcq(prob, question_id=qid))

    # Filter on a saved column: force a case where A is NOT revealed preferred to B
    prob = REGISTRY.sample_problem("RevealedPreference", rng=rng, name="rp4", A_rp_B=False)
    assert prob.sol["A_rp_B"] is False
    exam.add(formats.get_single_mcq(prob, question_id=1))

    exam.add(RawLatex("\\noindent\\textbf{Part II: Short answer}\n"))

    # 5. Multipart short answer (a./b. list)
    sa_prob = REGISTRY.sample_problem("RevealedPreference", rng=rng, name="rp5")
    exam.add(formats.get_multipart_sa(sa_prob))

    return exam, sa_prob


def main():
    assert "RevealedPreference" in REGISTRY, REGISTRY.names()

    rng = np.random.default_rng(0)
    exam, sa_prob = build_exam(rng)

    tex = exam.texify()
    sol_tex = exam.texify(solutions=True)
    assert "Answer:" not in tex
    assert sol_tex.count("Answer:") == 5  # 2 (multipart) + 3 (single) MCQs
    assert sa_prob.setup_list[0]["setup"] in tex

    # Reproducibility: same seed -> same exam
    exam2, _ = build_exam(np.random.default_rng(0))
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
