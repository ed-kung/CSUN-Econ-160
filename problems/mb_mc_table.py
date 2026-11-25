import numpy as np
from econtools.problems.base import MCQ, GenericProblem, generate_distractors
from econtools.tables.tables import Table

class MBMCTable(GenericProblem):
    default_params = {
        "type": "cars",
        "name": "Stan's Used Car Rentals",
        "MB": [25, 20, 15, 10, 5],
        "MC": [15, 16, 17, 18, 19]
    }

    # Random Problem Generator (see problems/_rpg.py)
    rpg_topic = "decisions-decisions"
    rpg_title = "2. Decisions Decisions"

    def build(self, rng):
        p = self.params
        MB = np.array(p['MB'])
        MC = np.array(p['MC'])
        MU = MB - MC
        TU = np.concatenate([[0], np.cumsum(MU)])  # TU[q] = total utility of choosing q (q = 0..N)
        choice = int(np.argmax(TU))
        utility = TU[choice]
        table_data = []
        table_data.append([p['type'].capitalize(), "Marginal Benefit", "Marginal Cost"])
        table_data.append(["0", "-", "-"])
        for i in range(len(MB)):
            table_data.append([i+1, MB[i], MC[i]])
        table = Table(table_data)
        self.sol = {'choice': choice, 'utility': utility, 'TU': TU}

        if p['type'] == 'cars':
            setup = f"{p['name']} is deciding how many cars to keep in its lot. The marginal benefit and marginal cost of keeping each additional car is shown in the table below. {p['name']} makes choices to maximize its utility, which equals the total benefit minus the total cost.\n\n"
            setup += table.texify()

            online_setup = f"<p>{p['name']} is deciding how many cars to keep in its lot. The marginal benefit and marginal cost of keeping each additional car is shown in the table below. {p['name']} makes choices to maximize its utility, which equals the total benefit minus the total cost.</p>"
            online_setup += "<p>" + table.htmlify() + "</p>"

        elif p['type'] == 'espresso machines':
            setup = f"{p['name']} is deciding how many espresso machines to purchase for its stores. The marginal benefit and marginal cost of purchasing each additional espresso machine is shown in the table below. {p['name']} makes choices to maximize its utility, which equals the total benefit minus the total cost.\n\n"
            setup += table.texify()

            online_setup = f"<p>{p['name']} is deciding how many espresso machines to purchase for its stores. The marginal benefit and marginal cost of purchasing each additional espresso machine is shown in the table below. {p['name']} makes choices to maximize its utility, which equals the total benefit minus the total cost.</p>"
            online_setup += "<p>" + table.htmlify() + "</p>"
        
        # --- setups ---
        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        if p['type'] == 'cars':
            q = "How many cars should be kept in the lot?"
        elif p['type'] == 'espresso machines':
            q = "How many espresso machines should be purchased?"
        a = self.sol['choice']
        answers = generate_distractors(a, K=4, delta=1, must_positive=True, rng=rng)
        mcq = MCQ(q, answers, solution=0, shuffle=False, sort=True, numerical=True, horz=True, rng=rng)
        self.add_question(q, a, mcq=mcq)

        q = "What is the total utility at the optimal choice?"
        a = self.sol['utility']
        answers = generate_distractors(a, K=4, must_positive=True, rng=rng)
        mcq = MCQ(q, answers, solution=0, shuffle=False, sort=True, numerical=True, horz=True, rng=rng)
        self.add_question(q, a, mcq=mcq)

    def check_solution(self):
        # no negative numbers in MB or MC
        MB = self.params['MB']
        MC = self.params['MC']
        if any(x < 0 for x in MB) or any(x < 0 for x in MC):
            return False
        # no ties in TU
        TU = self.sol['TU']
        if len(TU) != len(set(TU)):
            return False
        # interior solution
        choice = self.sol['choice']
        if choice == 0 or choice == len(MB):
            return False
        return True
    
    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 100
        # ---- cars ----
        type = 'cars'
        names = [
            "Stan's Used Car Rentals",
            "Bob's Car Emporium",
            "Kenny's Car Lot"
        ]
        for i in range(N_SAMPLES):
            name = names[rng.choice(len(names))]
            n_choices = rng.integers(5, 8)
            MB_intercept = rng.integers(25, 51)
            MB_slope = rng.integers(-5, 0)
            MC_intercept = rng.integers(0, 26)
            MC_slope = rng.integers(1, 6)
            MB = MB_intercept + MB_slope * (np.arange(n_choices) + 1)
            MC = MC_intercept + MC_slope * (np.arange(n_choices) + 1)
            yield {
                'type': type,
                'name': name,
                'MB': MB.tolist(),
                'MC': MC.tolist()
            }
        # --- espresso machines ----
        type = 'espresso machines'
        names = [
            "Coffee Bean",
            "Starbucks",
            "Dunkin Donuts"
        ]
        for i in range(N_SAMPLES):
            name = names[rng.choice(len(names))]
            n_choices = rng.integers(5, 8)
            MB_intercept = rng.integers(25, 51)
            MB_slope = rng.integers(-5, 0)
            MC_intercept = rng.integers(0, 26)
            MC_slope = rng.integers(1, 6)
            MB = MB_intercept + MB_slope * (np.arange(n_choices) + 1)
            MC = MC_intercept + MC_slope * (np.arange(n_choices) + 1)
            yield {
                'type': type,
                'name': name,
                'MB': MB.tolist(),
                'MC': MC.tolist()
            }




