"""Revealed preference problems (placeholder content)."""

import itertools

from econtools.problems.base import MCQ, GenericProblem, generate_distractors


class RevealedPreference(GenericProblem):
    default_params = {"p1": 2, "p2": 3, "x1A": 4, "x2A": 2, "x1B": 2, "x2B": 3}

    # Random Problem Generator (see problems/_rpg.py)
    rpg_topic = "revealed-preference"
    rpg_title = "Revealed Preference"

    def build(self, rng):
        p = self.params
        cost_A = p["p1"] * p["x1A"] + p["p2"] * p["x2A"]
        cost_B = p["p1"] * p["x1B"] + p["p2"] * p["x2B"]
        self.sol = {
            "cost_A": int(cost_A),
            "cost_B": int(cost_B),
            "A_rp_B": bool(cost_B < cost_A),
        }

        # --- setups ---
        self.add_setup(
            f"At prices $p_1={p['p1']}$ and $p_2={p['p2']}$, a consumer chooses bundle "
            f"$A=({p['x1A']},{p['x2A']})$ when bundle $B=({p['x1B']},{p['x2B']})$ "
            f"is also available."
        )

        # --- questions ---
        # 0: cost of bundle B (numerical MCQ)
        q = "How much does bundle $B$ cost at these prices?"
        answers = generate_distractors(cost_B, K=4, rng=rng, must_positive=True)
        self.add_question(
            q, f"${cost_B}$",
            mcq=MCQ(q, answers, solution=0, numerical=True, rng=rng),
        )

        # 1: revealed preference (yes/no MCQ)
        q = "Is $A$ directly revealed preferred to $B$?"
        yes = self.sol["A_rp_B"]
        self.add_question(
            q, "Yes" if yes else "No",
            mcq=MCQ(q, ["Yes", "No"], solution=0 if yes else 1, shuffle=False, rng=rng),
        )

    def check_solution(self):
        # Reject ties and identical bundles.
        p = self.params
        return (
            self.sol["cost_A"] != self.sol["cost_B"]
            and (p["x1A"], p["x2A"]) != (p["x1B"], p["x2B"])
        )

    @classmethod
    def candidate_params(cls, rng):
        r = range(1, 6)
        for p1, p2, x1A, x2A, x1B, x2B in itertools.product(r, r, r, r, r, r):
            yield {"p1": p1, "p2": p2, "x1A": x1A, "x2A": x2A, "x1B": x1B, "x2B": x2B}
