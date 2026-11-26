import numpy as np
from econtools.entities import Country, Good
from econtools.problems.base import MCQ, GenericProblem, generate_distractors
from econtools.math.scaled import Scaled

class Specialization2(GenericProblem):
    default_params = {
        'countries': (Country.get('China'), Country.get('America')),
        'good_1': Good.get('car'),
        'good_2': Good.get('movie'),
        'good_1_cost': (10_000, 20_000),
        'good_2_cost': (1_000_000, 1_500_000),
    }
    rpg_topic = "specialization-trade"
    rpg_title = "3. Specialization and Trade"

    def build(self, rng):
        p = self.params
        names = tuple(country.name for country in p['countries'])
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
            person_1_specialization = good_1.plural
            person_2_specialization = good_2.plural
        else:
            comparative_advantage_good_1 = names[1]
            comparative_advantage_good_2 = names[0]
            person_1_specialization = good_2.plural
            person_2_specialization = good_1.plural
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
        setup = f"It costs {names[0]} {Scaled(good_1_cost[0],1,'$').texify()} to produce {good_1.a} and {Scaled(good_2_cost[0],1,'$').texify()} to produce {good_2.a}. It costs {names[1]} {Scaled(good_1_cost[1],1,'$').texify()} to produce {good_1.a} and {Scaled(good_2_cost[1],1,'$').texify()} to produce {good_2.a}."
        online_setup = f"It costs {names[0]} {str(Scaled(good_1_cost[0],1,'$'))} to produce {good_1.a} and {str(Scaled(good_2_cost[0],1,'$'))} to produce {good_2.a}. It costs {names[1]} {str(Scaled(good_1_cost[1],1,'$'))} to produce {good_1.a} and {str(Scaled(good_2_cost[1],1,'$'))} to produce {good_2.a}."
        self.add_setup(setup=setup, online_setup=online_setup)

        # ---- questions ----
        q = f"What is {names[0]}'s opportunity cost of producing {good_1.plural}, in units of {good_2.plural} foregone per unit of {good_1.plural} produced?"
        a = self.sol['opp_cost_good_1_person_1']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[0]}'s opportunity cost of producing {good_2.plural}, in units of {good_1.plural} foregone per unit of {good_2.plural} produced?"
        a = self.sol['opp_cost_good_2_person_1']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[1]}'s opportunity cost of producing {good_1.plural}, in units of {good_2.plural} foregone per unit of {good_1.plural} produced?"
        a = self.sol['opp_cost_good_1_person_2']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[1]}'s opportunity cost of producing {good_2.plural}, in units of {good_1.plural} foregone per unit of {good_2.plural} produced?"
        a = self.sol['opp_cost_good_2_person_2']
        self.add_numeric_question(q, a, rng=rng)

        question = f"\\underline{{\\hspace{{2cm}}}} has a comparative advantage in producing {good_1.plural} and \\underline{{\\hspace{{2cm}}}} has a comparative advantage in producing {good_2.plural}."
        online_question = f"______ has a comparative advantage in producing {good_1.plural} and ______ has a comparative advantage in producing {good_2.plural}."
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

        question = f"\\underline{{\\hspace{{2cm}}}} has an absolute advantage in producing {good_1.plural} and \\underline{{\\hspace{{2cm}}}} has an absolute advantage in producing {good_2.plural}."
        online_question = f"______ has an absolute advantage in producing {good_1.plural} and ______ has an absolute advantage in producing {good_2.plural}."
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
            f"{good_1.plural}, {good_1.plural}",
            f"{good_1.plural}, {good_2.plural}",
            f"{good_2.plural}, {good_1.plural}",
            f"{good_2.plural}, {good_2.plural}"
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
        # costs are a grid value (COST_GRID) times the good's typical price scale (goods.csv)
        COST_GRID = (1, 11)
        for i in range(N_SAMPLES):
            countries = Country.sample(rng, 2)
            good_1, good_2 = Good.sample(rng, 2, tags='traded')
            good_1_cost = tuple(int(rng.integers(*COST_GRID)) * good_1.pscale for _ in range(2))
            good_2_cost = tuple(int(rng.integers(*COST_GRID)) * good_2.pscale for _ in range(2))
            if good_1_cost[0]/good_2_cost[0] == good_1_cost[1]/good_2_cost[1]:
                continue
            if good_1_cost[0] == good_2_cost[0]:
                continue
            if good_1_cost[1] == good_2_cost[1]:
                continue
            yield {
                'countries': countries,
                'good_1': good_1,
                'good_2': good_2,
                'good_1_cost': good_1_cost,
                'good_2_cost': good_2_cost
            }



