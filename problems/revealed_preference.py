"""Revealed preference problems (placeholder content)."""

import itertools

from econtools.problems.base import MCQ, GenericProblem, generate_distractors
from econtools.tables.tables import Table


class RevealedPreference(GenericProblem):
    default_params = {
        "type": "day off",
        "name": "Ferris",
        "pronouns": ["he", "his"],
        "table": [
            ["stay home", 50, 0],
            ["run errands", 40, 10],
            ["visit the museum", 80, 15],
            ["go to the baseball game", 120, 40]
        ],
        "masked_choice_idx": 0
    }

    # Random Problem Generator (see problems/_rpg.py)
    rpg_topic = "revealed-preference"
    rpg_title = "Revealed Preference"

    def build(self, rng):
        p = self.params
        table = Table(p['table'], masked=[ (p['masked_choice'], 1) ])
        utils = [p['table'][i][1] - p['table'][i][2] for i in range(len(p['table']))]
        utils_ranked_idx = sorted(range(len(utils)), key=lambda i: utils[i], reverse=True)
        utils_ranked = [utils[i] for i in utils_ranked_idx]
        choices_ranked = [p['table'][i][0] for i in utils_ranked_idx]
        best_choice_idx = utils_ranked_idx[0]
        best_choice_str = choices_ranked[0]
        best_choice_util = utils_ranked[0]
        best_choice_benefit = p['table'][best_choice_idx][1]
        masked_choice_idx = p['masked_choice_idx']
        masked_choice_str = p['table'][masked_choice_idx][0]
        masked_choice_cost = p['table'][masked_choice_idx][2]
        second_best_choice_idx = utils_ranked_idx[1]
        second_best_choice_str = choices_ranked[0]
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
            setup = f"{p['name']} has a day off. {p['pronouns'][0]} can either {p['table'][0][0]}, {p['table'][1][0]}, {p['table'][2][0]}, or {p['table'][3][0]}. {p['name']}'s costs and benefits for each option are shown in the table below. {p['name']} makes choices to maximize {p['prnouns'][1]} utility, which equals benefit minus cost.\n\n"
            setup += table.texify() + "\n\n"
            setup += f"Suppose {p['name']} chooses to {best_choice_str}. Then {p['name']}'s benefit of ``{masked_choice_str}'' must be \\underline{{\\hspace{{3cm}}}}."

            online_setup = f"<p>{p['name']} has a day off. {p['pronouns'][0]} can either {p['table'][0][0]}, {p['table'][1][0]}, {p['table'][2][0]}, or {p['table'][3][0]}. {p['name']}'s costs and benefits for each option are shown in the table below. {p['name']} makes choices to maximize {p['prnouns'][1]} utility, which equals benefit minus cost.</p>"
            online_setup += "<p>" + table.htmlify() + "</p>"
            online_setup += f"<p>Suppose {p['name']} chooses to {best_choice_str}. Then {p['name']}'s benefit of ``{masked_choice_str}'' must be ______.</p>"

        # --- setups ---
        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        q = "Fill in the first part of the blank."
        a = ans_1
        answers = ['at most', 'at least']
        ans_idx = answers.index(ans_1)
        self.add_question(q, a, mcq=MCQ(q, answers, solution=ans_idx, shuffle=False, horz=True, rng=rng))

        q = "Fill in the second part of the blank."
        a = ans_2
        answers = generate_distractors(ans_2, K=4, rng=rng, must_positive=True)
        self.add_question(q, a, mcq=MCQ(q, answers, solution=0, numerical=True, sort=True, rng=rng))

    def check_solution(self):
        # check no ties in utils_ranked
        utils_ranked = self.sol['utils_ranked']
        if len(utils_ranked) != len(set(utils_ranked)):
            return False
        return True

    @classmethod
    def candidate_params(cls, rng):
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
            (name, pronouns) = rng.choice(names)
            my_choices = rng.choice(choices, size=4, replace=False)
            masked_choice_idx = rng.choice(range(4))
            table = []
            for choice in my_choices:
                table.append([choice[0], rng.randint(choice[1][0], choice[1][1]+1), rng.randint(choice[2][0], choice[2][1]+1)])
            yield {
                'type': type,
                'name': name,
                'pronouns': pronouns,
                'table': table,
                'masked_choice_idx': masked_choice_idx
            }

