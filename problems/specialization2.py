import numpy as np
from econtools.problems.base import MCQ, GenericProblem, generate_distractors
from econtools.math.scaled import Scaled

class Specialization2(GenericProblem):
    default_params = {
        'names': ('China', 'America'),
        'good_1': ('car', 'cars'),
        'good_2': ('movie', 'movies'),
        'good_1_cost': (10_000, 20_000),
        'good_2_cost': (1_000_000, 1_500_000),
    }
    rpg_topic = "specialization-trade"
    rpg_title = "3. Specialization and Trade"

    def build(self, rng):
        p = self.params
        names = p['names']
        good_1 = p['good_1']
        good_2 = p['good_2']
        good_1_cost = p['good_1_cost']
        good_2_cost = p['good_2_cost']
        opp_cost_good_1_person_1 = good_1_cost[0] / good_2_cost[0]
        opp_cost_good_1_person_2 = good_1_cost[1] / good_2_cost[1]
        opp_cost_good_2_person_1 = good_2_cost[0] / good_1_cost[0]
        opp_cost_good_2_person_2 = good_2_cost[1] / good_1_cost[1]
        if opp_cost_good_1_person_1 < opp_cost_good_1_person_2:
            comparative_advantage_good_1 = names[0]
            comparative_advantage_good_2 = names[1]
            person_1_specialization = good_1[1]
            person_2_specialization = good_2[1]
        else:
            comparative_advantage_good_1 = names[1]
            comparative_advantage_good_2 = names[0]
            person_1_specialization = good_2[1]
            person_2_specialization = good_1[1]
        if good_1_cost[0] > good_1_cost[1]:
            absolute_advantage_good_1 = names[1]
        else:
            absolute_advantage_good_1 = names[0]
        if good_2_cost[0] > good_2_cost[1]:
            absolute_advantage_good_2 = names[1]
        else:
            absolute_advantage_good_2 = names[0]

        self.sol = {
            'opp_cost_good_1_person_1': opp_cost_good_1_person_1,
            'opp_cost_good_1_person_2': opp_cost_good_1_person_2,
            'opp_cost_good_2_person_1': opp_cost_good_2_person_1,
            'opp_cost_good_2_person_2': opp_cost_good_2_person_2,
            'comparative_advantage_good_1': comparative_advantage_good_1,
            'comparative_advantage_good_2': comparative_advantage_good_2,
            'absolute_advantage_good_1': absolute_advantage_good_1,
            'absolute_advantage_good_2': absolute_advantage_good_2,
            'person_1_specialization': person_1_specialization,
            'person_2_specialization': person_2_specialization,
        }

        # ---- setups ----
        setup = f"It costs {names[0]} {Scaled(good_1_cost[0],1,'$').texify()} to produce a {good_1[0]} and {Scaled(good_2_cost[0],1,'$').texify()} to produce a {good_2[0]}. It costs {names[1]} {Scaled(good_1_cost[1],1,'$').texify()} to produce a {good_1[0]} and {Scaled(good_2_cost[1],1,'$').texify()} to produce a {good_2[0]}."
        online_setup = f"It costs {names[0]} {str(Scaled(good_1_cost[0],1,'$'))} to produce a {good_1[0]} and {str(Scaled(good_2_cost[0],1,'$'))} to produce a {good_2[0]}. It costs {names[1]} {str(Scaled(good_1_cost[1],1,'$'))} to produce a {good_1[0]} and {str(Scaled(good_2_cost[1],1,'$'))} to produce a {good_2[0]}."
        self.add_setup(setup=setup, online_setup=online_setup)

        # ---- questions ----
        q = f"What is {names[0]}'s opportunity cost of producing {good_1[1]}, in units of {good_2[1]} foregone per unit of {good_1[1]} produced?"
        a = self.sol['opp_cost_good_1_person_1']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[0]}'s opportunity cost of producing {good_2[1]}, in units of {good_1[1]} foregone per unit of {good_2[1]} produced?"
        a = self.sol['opp_cost_good_2_person_1']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[1]}'s opportunity cost of producing {good_1[1]}, in units of {good_2[1]} foregone per unit of {good_1[1]} produced?"
        a = self.sol['opp_cost_good_1_person_2']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[1]}'s opportunity cost of producing {good_2[1]}, in units of {good_1[1]} foregone per unit of {good_2[1]} produced?"
        a = self.sol['opp_cost_good_2_person_2']
        self.add_numeric_question(q, a, rng=rng)

        question = f"\\underline{{\\hspace{{2cm}}}} has a comparative advantage in producing {good_1[1]} and \\underline{{\\hspace{{2cm}}}} has a comparative advantage in producing {good_2[1]}."
        online_question = f"______ has a comparative advantage in producing {good_1[1]} and ______ has a comparative advantage in producing {good_2[1]}."
        answers = [
            f"{names[0]}, {names[0]}",
            f"{names[0]}, {names[1]}",
            f"{names[1]}, {names[0]}",
            f"{names[1]}, {names[1]}"
        ]
        answer = f"{self.sol['comparative_advantage_good_1']}, {self.sol['comparative_advantage_good_2']}"
        sol = answers.index(answer)
        mcq = MCQ(question, answers, solution=sol, shuffle=False, horz=False, rng=rng)
        self.add_question(question=question, online_question=online_question, answer=answer, mcq=mcq)

        question = f"\\underline{{\\hspace{{2cm}}}} has an absolute advantage in producing {good_1[1]} and \\underline{{\\hspace{{2cm}}}} has an absolute advantage in producing {good_2[1]}."
        online_question = f"______ has an absolute advantage in producing {good_1[1]} and ______ has an absolute advantage in producing {good_2[1]}."
        answers = [
            f"{names[0]}, {names[0]}",
            f"{names[0]}, {names[1]}",
            f"{names[1]}, {names[0]}",
            f"{names[1]}, {names[1]}"
        ]
        answer = f"{self.sol['absolute_advantage_good_1']}, {self.sol['absolute_advantage_good_2']}"
        sol = answers.index(answer)
        mcq = MCQ(question, answers, solution=sol, shuffle=False, horz=False, rng=rng)
        self.add_question(question=question, online_question=online_question, answer=answer, mcq=mcq)

        question = f"{names[0]} should export \\underline{{\\hspace{{2cm}}}} to {names[1]} and {names[1]} should export \\underline{{\\hspace{{2cm}}}} to {names[0]}."
        online_question = f"{names[0]} should export ______ to {names[1]} and {names[1]} should export ______ to {names[0]}."
        answers = [
            f"{good_1[1]}, {good_1[1]}",
            f"{good_1[1]}, {good_2[1]}",
            f"{good_2[1]}, {good_1[1]}",
            f"{good_2[1]}, {good_2[1]}"
        ]
        answer = f"{self.sol['person_1_specialization']}, {self.sol['person_2_specialization']}"
        sol = answers.index(answer)
        mcq = MCQ(question, answers, solution=sol, shuffle=False, horz=False, rng=rng)
        self.add_question(question=question, online_question=online_question, answer=answer, mcq=mcq)


    def check_solution(self):
        if self.sol['opp_cost_good_1_person_1'] == self.sol['opp_cost_good_1_person_2']:
            return False
        if self.params['good_1_cost'][0] == self.params['good_1_cost'][1]:
            return False
        if self.params['good_2_cost'][0] == self.params['good_2_cost'][1]:
            return False
        return True

    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        names = ['America', 'China', 'Taiwan', 'Mexico', 'Brazil', 'France', 'Germany', 'Japan', 'Korea']
        goods = [
            ('car', 'cars', 2, 7, 10_000),
            ('movie', 'movies', 1, 10, 500_000),
            ('sneaker', 'sneakers', 1, 10, 5),
            ('computer', 'computers', 1, 11, 100),
            ('smartphone', 'smartphones', 1, 11, 100),
            ('t-shirt', 't-shirts', 1, 11, 10)
        ]
        for i in range(N_SAMPLES):
            my_names = tuple(rng.choice(names, size=2, replace=False))
            idx = rng.choice(len(goods), size=2, replace=False)
            my_goods = [goods[i] for i in idx]
            good_1 = (my_goods[0][0], my_goods[0][1])
            good_2 = (my_goods[1][0], my_goods[1][1])
            good_1_cost_min = my_goods[0][2]
            good_2_cost_min = my_goods[1][2]
            good_1_cost_max = my_goods[0][3] + 1
            good_2_cost_max = my_goods[1][3] + 1
            good_1_cost_scale = my_goods[0][4]
            good_2_cost_scale = my_goods[1][4]
            good_1_cost = (
                rng.integers(good_1_cost_min, good_1_cost_max) * good_1_cost_scale,
                rng.integers(good_1_cost_min, good_1_cost_max) * good_1_cost_scale
            )
            good_2_cost = (
                rng.integers(good_2_cost_min, good_2_cost_max) * good_2_cost_scale,
                rng.integers(good_2_cost_min, good_2_cost_max) * good_2_cost_scale
            )
            if good_1_cost[0]/good_2_cost[0] == good_1_cost[1]/good_2_cost[1]:
                continue
            if good_1_cost[0] == good_2_cost[0]:
                continue
            if good_1_cost[1] == good_2_cost[1]:
                continue
            yield {
                'names': my_names,
                'good_1': good_1,
                'good_2': good_2,
                'good_1_cost': good_1_cost,
                'good_2_cost': good_2_cost
            }



