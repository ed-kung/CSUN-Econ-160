from econtools.problems.base import MCQ, GenericProblem, generate_distractors
from econtools.tables.tables import Table


def dollars(x, online=False):
    """Format a dollar amount with thousands separators: $1,234 (or $1,234.50 if fractional).

    LaTeX needs the sign escaped (\\$). Online, it is written as the HTML entity &#36;
    so that problems/_rpg.to_mathjax doesn't read a pair of dollar signs as inline math.
    """
    x = float(x)
    num = f"{abs(x):,.0f}" if x.is_integer() else f"{abs(x):,.2f}"
    sign = "-" if x < 0 else ""
    return sign + ("&#36;" if online else "\\$") + num


class RevealedPreference(GenericProblem):
    default_params = {
        "type": "day off",
        "name": "Ferris",
        "pronouns": ["he", "his"],
        # one entry per option; kept as separate same-typed lists so they store cleanly in parquet
        "options": ["stay home", "run errands", "visit the museum", "go to the baseball game"],
        "benefits": [50, 40, 80, 120],
        "costs": [0, 10, 15, 40],
        "masked_choice_idx": 0
    }

    # Random Problem Generator (see problems/_rpg.py)
    rpg_topic = "revealed-preference"
    rpg_title = "Revealed Preference"

    def build(self, rng):
        p = self.params
        # params loaded from parquet come back as numpy arrays/ints; normalize to plain Python
        options = [str(x) for x in p['options']]
        benefits = [int(x) for x in p['benefits']]
        costs = [int(x) for x in p['costs']]
        masked = [ (int(p['masked_choice_idx']) + 1, 1) ]  # +1 for header row
        header = [["Option", "Benefit", "Cost"]]
        table = Table(header + [[o, dollars(b), dollars(c)] for o, b, c in zip(options, benefits, costs)], masked=masked)
        online_table = Table(header + [[o, dollars(b, online=True), dollars(c, online=True)] for o, b, c in zip(options, benefits, costs)], masked=masked)
        utils = [b - c for b, c in zip(benefits, costs)]
        utils_ranked_idx = sorted(range(len(utils)), key=lambda i: utils[i], reverse=True)
        utils_ranked = [utils[i] for i in utils_ranked_idx]
        choices_ranked = [options[i] for i in utils_ranked_idx]
        best_choice_idx = utils_ranked_idx[0]
        best_choice_str = choices_ranked[0]
        best_choice_util = utils_ranked[0]
        best_choice_benefit = benefits[best_choice_idx]
        masked_choice_idx = int(p['masked_choice_idx'])
        masked_choice_str = options[masked_choice_idx]
        masked_choice_cost = costs[masked_choice_idx]
        second_best_choice_idx = utils_ranked_idx[1]
        second_best_choice_str = choices_ranked[1]
        second_best_choice_util = utils_ranked[1]

        if masked_choice_idx == best_choice_idx:
            # the masked choice is the best choice, so the utility must be at least as high as the second best choice
            ans_1 = 'at least'
            ans_2 = second_best_choice_util + masked_choice_cost
        else:
            # the masked choice is not the best choice, so the utility must be less than the best choice
            ans_1 = 'at most'
            ans_2 = best_choice_util + masked_choice_cost
        
        self.sol = {'ans_1': ans_1, 'ans_2': ans_2, 'utils_ranked': utils_ranked, 'choices_ranked': choices_ranked}

        if p["type"] == "day off":
            setup = f"{p['name']} has a day off. {p['pronouns'][0].capitalize()} can either {options[0]}, {options[1]}, {options[2]}, or {options[3]}. {p['name']}'s costs and benefits for each option are shown in the table below. {p['name']} makes choices to maximize {p['pronouns'][1]} utility, which equals benefit minus cost.\n\n"
            setup += table.texify() + "\n\n"
            setup += f"Suppose {p['name']} chooses to {best_choice_str}. Then {p['name']}'s benefit of ``{masked_choice_str}'' must be \\underline{{\\hspace{{3cm}}}}."

            online_setup = f"<p>{p['name']} has a day off. {p['pronouns'][0].capitalize()} can either {options[0]}, {options[1]}, {options[2]}, or {options[3]}. {p['name']}'s costs and benefits for each option are shown in the table below. {p['name']} makes choices to maximize {p['pronouns'][1]} utility, which equals benefit minus cost.</p>"
            online_setup += "<p>" + online_table.htmlify() + "</p>"
            online_setup += f"<p>Suppose {p['name']} chooses to {best_choice_str}. Then {p['name']}'s benefit of \"{masked_choice_str}\" must be ______.</p>"
        
        elif p["type"] == "lunch":
            setup = f"{p['name']} is deciding what to eat for lunch. The choices are {options[0]}, {options[1]}, {options[2]}, or {options[3]}. {p['name']}'s costs and benefits for each option are shown in the table below. {p['name']} makes choices to maximize {p['pronouns'][1]} utility, which equals benefit minus cost.\n\n"
            setup += table.texify() + "\n\n"
            setup += f"Suppose {p['name']} chooses {best_choice_str}. Then {p['name']}'s benefit of ``{masked_choice_str}'' must be \\underline{{\\hspace{{3cm}}}}."

            online_setup = f"<p>{p['name']} is deciding what to eat for lunch. The choices are {options[0]}, {options[1]}, {options[2]}, or {options[3]}. {p['name']}'s costs and benefits for each option are shown in the table below. {p['name']} makes choices to maximize {p['pronouns'][1]} utility, which equals benefit minus cost.</p>"
            online_setup += "<p>" + online_table.htmlify() + "</p>"
            online_setup += f"<p>Suppose {p['name']} chooses {best_choice_str}. Then {p['name']}'s benefit of \"{masked_choice_str}\" must be ______.</p>"

        # --- setups ---
        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        q = "Fill in the first part of the blank."
        a = ans_1
        answers = ['at most', 'at least']
        ans_idx = answers.index(ans_1)
        self.add_question(q, a, mcq=MCQ(q, answers, solution=ans_idx, shuffle=False, horz=True, rng=rng))

        q = "Fill in the second part of the blank."
        # sort numerically before formatting (sorting the strings would put "$1,000" before "$900")
        values = sorted(generate_distractors(ans_2, K=4, rng=rng, must_positive=True))
        answers = [dollars(v) for v in values]
        mcq = MCQ(q, answers, solution=values.index(ans_2), shuffle=False, rng=rng)
        self.add_question(q, dollars(ans_2), online_answer=dollars(ans_2, online=True), mcq=mcq)

    def check_solution(self):
        # check no ties in utils_ranked
        utils_ranked = self.sol['utils_ranked']
        if len(utils_ranked) != len(set(utils_ranked)):
            return False
        return True

    @classmethod
    def candidate_params(cls, rng):
        # ---- Day off ----
        type = 'day off'
        names = [
            ('Ferris', ['he', 'his']),
            ('Jane', ['she', 'her'])
        ]
        choices = [
            # [name, (min_benefit, max_benefit), (min_cost, max_cost)]
            ['stay home', (10, 50), (0, 0)],
            ['run errands', (20, 60), (5, 20)],
            ['visit the museum', (30, 100), (10, 50)],
            ['go to the baseball game', (50, 150), (20, 80)],
            ['go to the beach', (40, 120), (10, 40)],
            ['watch a movie', (30, 100), (10, 40)]
        ]
        # yield 200 examples
        for i in range(200):
            (name, pronouns) = names[rng.choice(len(names))]
            my_choices = [choices[j] for j in rng.choice(len(choices), size=4, replace=False)]
            masked_choice_idx = int(rng.choice(4))
            options, benefits, costs = [], [], []
            for choice in my_choices:
                options.append(choice[0])
                benefits.append(int(rng.integers(choice[1][0], choice[1][1]+1)))
                costs.append(int(rng.integers(choice[2][0], choice[2][1]+1)))
            yield {
                'type': type,
                'name': name,
                'pronouns': pronouns,
                'options': options,
                'benefits': benefits,
                'costs': costs,
                'masked_choice_idx': masked_choice_idx
            }

        # ---- Lunch ----
        type = 'lunch'
        names = [
            ('Alice', ['she', 'her']),
            ('John', ['he', 'his'])
        ]
        choices = [
            # [name, (min_benefit, max_benefit), (min_cost, max_cost)]
            ['salad', (5, 20), (4, 10)],
            ['sandwich', (5, 20), (4, 10)],
            ['pizza', (5, 20), (4, 10)],
            ['burger', (5, 20), (4, 10)],
            ['pasta', (5, 20), (4, 10)],
            ['burrito', (5, 20), (4, 10)]
        ]
        # yield 200 examples
        for i in range(200):
            (name, pronouns) = names[rng.choice(len(names))]
            my_choices = [choices[j] for j in rng.choice(len(choices), size=4, replace=False)]
            masked_choice_idx = int(rng.choice(4))
            options, benefits, costs = [], [], []
            for choice in my_choices:
                options.append(choice[0])
                benefits.append(int(rng.integers(choice[1][0], choice[1][1]+1)))
                costs.append(int(rng.integers(choice[2][0], choice[2][1]+1)))
            yield {
                'type': type,
                'name': name,
                'pronouns': pronouns,
                'options': options,
                'benefits': benefits,
                'costs': costs,
                'masked_choice_idx': masked_choice_idx
            }
