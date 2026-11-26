import numpy as np
from econtools.entities import Country, Good
from econtools.problems.base import MCQ, GenericProblem, generate_distractors
from econtools.math.scaled import Scaled

class Specialization2(GenericProblem):
    default_params = {
        'countries': (Country.get('China'), Country.get('America')),
        'good_1': Good.get('cars'),
        'good_2': Good.get('computers'),
        'good_1_cost': (10_000, 20_000),
        'good_2_cost': (1_000, 1_500),
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
            person_1_specialization = good_1.market
            person_2_specialization = good_2.market
        else:
            comparative_advantage_good_1 = names[1]
            comparative_advantage_good_2 = names[0]
            person_1_specialization = good_2.market
            person_2_specialization = good_1.market
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
        def costs(fmt):
            sentences = []
            for k in range(2):
                c1, c2 = fmt(good_1_cost[k]), fmt(good_2_cost[k])
                sentences.append(f"{names[k]} can produce {good_1.market} at a cost of {c1} per {good_1.singular} "
                                 f"and {good_2.market} at a cost of {c2} per {good_2.singular}.")
            return " ".join(sentences)
        setup = costs(lambda c: Scaled(c, 1, '$').texify())
        online_setup = costs(lambda c: str(Scaled(c, 1, '$')))
        self.add_setup(setup=setup, online_setup=online_setup)

        # ---- questions ----
        q = f"What is {names[0]}'s opportunity cost of producing {good_1.market}, in {good_2.units} foregone per {good_1.unit} produced?"
        a = self.sol['opp_cost_good_1_person_1']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[0]}'s opportunity cost of producing {good_2.market}, in {good_1.units} foregone per {good_2.unit} produced?"
        a = self.sol['opp_cost_good_2_person_1']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[1]}'s opportunity cost of producing {good_1.market}, in {good_2.units} foregone per {good_1.unit} produced?"
        a = self.sol['opp_cost_good_1_person_2']
        self.add_numeric_question(q, a, rng=rng)

        q = f"What is {names[1]}'s opportunity cost of producing {good_2.market}, in {good_1.units} foregone per {good_2.unit} produced?"
        a = self.sol['opp_cost_good_2_person_2']
        self.add_numeric_question(q, a, rng=rng)

        question = f"\\underline{{\\hspace{{2cm}}}} has a comparative advantage in producing {good_1.market} and \\underline{{\\hspace{{2cm}}}} has a comparative advantage in producing {good_2.market}."
        online_question = f"______ has a comparative advantage in producing {good_1.market} and ______ has a comparative advantage in producing {good_2.market}."
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

        question = f"\\underline{{\\hspace{{2cm}}}} has an absolute advantage in producing {good_1.market} and \\underline{{\\hspace{{2cm}}}} has an absolute advantage in producing {good_2.market}."
        online_question = f"______ has an absolute advantage in producing {good_1.market} and ______ has an absolute advantage in producing {good_2.market}."
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
            f"{good_1.market}, {good_1.market}",
            f"{good_1.market}, {good_2.market}",
            f"{good_2.market}, {good_1.market}",
            f"{good_2.market}, {good_2.market}"
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
        # costs are drawn from each good's price range in goods.csv (pmin..pmax times pscale)
        for i in range(N_SAMPLES):
            countries = Country.sample(rng, 2)
            good_1, good_2 = Good.sample(rng, 2, tags='market')
            good_1_cost = (good_1.random_price(rng), good_1.random_price(rng))
            good_2_cost = (good_2.random_price(rng), good_2.random_price(rng))
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



