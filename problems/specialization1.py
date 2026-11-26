import numpy as np
from econtools.entities import Good, Person
from econtools.problems.base import MCQ, GenericProblem, generate_distractors

class Specialization1(GenericProblem):
    default_params = {
        'type': 'lunch',
        'people': (Person.get('Bill'), Person.get('Ted')),
        'good_1': Good.get('pizza'),
        'good_2': Good.get('tacos'),
        'good_1_rate': (4, 2),
        'good_2_rate': (1, 2),
        'time_units': 'minute',
        'total_time': 10
    }
    rpg_topic = "specialization-trade"
    rpg_title = "3. Specialization and Trade"

    def build(self, rng):
        p = self.params
        type = p['type']
        names = tuple(person.name for person in p['people'])
        good_1 = p['good_1']
        good_2 = p['good_2']
        good_1_rate = p['good_1_rate']
        good_2_rate = p['good_2_rate']
        time_units = p['time_units']
        total_time = p['total_time']
        opp_cost_good_1_person_1 = good_2_rate[0] / good_1_rate[0]
        opp_cost_good_1_person_2 = good_2_rate[1] / good_1_rate[1]
        opp_cost_good_2_person_1 = good_1_rate[0] / good_2_rate[0]
        opp_cost_good_2_person_2 = good_1_rate[1] / good_2_rate[1]
        if opp_cost_good_1_person_1 < opp_cost_good_1_person_2:
            comparative_advantage_good_1 = names[0]
            comparative_advantage_good_2 = names[1]
            specialized_production_good_1 = good_1_rate[0] * total_time
            specialized_production_good_2 = good_2_rate[1] * total_time
            suboptimal_production_good_1 = good_2_rate[0] * total_time
            suboptimal_production_good_2 = good_1_rate[1] * total_time
        else:
            comparative_advantage_good_1 = names[1]
            comparative_advantage_good_2 = names[0]
            specialized_production_good_1 = good_1_rate[1] * total_time
            specialized_production_good_2 = good_2_rate[0] * total_time
            suboptimal_production_good_1 = good_2_rate[1] * total_time
            suboptimal_production_good_2 = good_1_rate[0] * total_time
        if good_1_rate[0] > good_1_rate[1]:
            absolute_advantage_good_1 = names[0]
        else:
            absolute_advantage_good_1 = names[1]
        if good_2_rate[0] > good_2_rate[1]:
            absolute_advantage_good_2 = names[0]
        else:
            absolute_advantage_good_2 = names[1]

        self.sol = {
            'opp_cost_good_1_person_1': opp_cost_good_1_person_1,
            'opp_cost_good_1_person_2': opp_cost_good_1_person_2,
            'opp_cost_good_2_person_1': opp_cost_good_2_person_1,
            'opp_cost_good_2_person_2': opp_cost_good_2_person_2,
            'comparative_advantage_good_1': comparative_advantage_good_1,
            'comparative_advantage_good_2': comparative_advantage_good_2,
            'absolute_advantage_good_1': absolute_advantage_good_1,
            'absolute_advantage_good_2': absolute_advantage_good_2,
            'specialized_production_good_1': specialized_production_good_1,
            'specialized_production_good_2': specialized_production_good_2,
            'suboptimal_production_good_1': suboptimal_production_good_1,
            'suboptimal_production_good_2': suboptimal_production_good_2
        }

        # ---- setups ----
        if type == 'lunch':
            setup = f"{names[0]} and {names[1]} each have {total_time} {time_units}s to make lunch. {names[0]} can produce {good_1.market} at a rate of {good_1.amount(good_1_rate[0], full=False)} per {time_units}, or {good_2.market} at a rate of {good_2.amount(good_2_rate[0], full=False)} per {time_units}. {names[1]} can produce {good_1.market} at a rate of {good_1.amount(good_1_rate[1], full=False)} per {time_units}, or {good_2.market} at a rate of {good_2.amount(good_2_rate[1], full=False)} per {time_units}."
        self.add_setup(setup=setup)

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

        question = f"\\underline{{\\hspace{{2cm}}}} should specialize in producing {good_1.market} and \\underline{{\\hspace{{2cm}}}} should specialize in producing {good_2.market}."
        online_question = f"______ should specialize in producing {good_1.market} and ______ should specialize in producing {good_2.market}."
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

        question = "If each person fully specializes in the good they have a comparative advantage in producing, how many of each good will be produced in the available time?"
        answers = [
            f"{good_1.amount(self.sol['specialized_production_good_1'])} and {good_2.amount(self.sol['specialized_production_good_2'])}",
            f"{good_1.amount(self.sol['specialized_production_good_1'])} and {good_2.amount(self.sol['suboptimal_production_good_2'])}",
            f"{good_1.amount(self.sol['suboptimal_production_good_1'])} and {good_2.amount(self.sol['specialized_production_good_2'])}",
            f"{good_1.amount(self.sol['suboptimal_production_good_1'])} and {good_2.amount(self.sol['suboptimal_production_good_2'])}"
        ]
        answer = answers[0]
        sol = 0
        mcq = MCQ(question, answers, solution=sol, shuffle=True, horz=False, rng=rng)
        self.add_question(question=question, answer=answer, mcq=mcq)

    def check_solution(self):
        if self.sol['opp_cost_good_1_person_1'] == self.sol['opp_cost_good_1_person_2']:
            return False
        if self.params['good_1_rate'][0] == self.params['good_1_rate'][1]:
            return False
        if self.params['good_2_rate'][0] == self.params['good_2_rate'][1]:
            return False
        return True

    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        type = "lunch"
        time_units = 'minute'
        for i in range(N_SAMPLES):
            people = Person.sample(rng, 2)
            my_goods = Good.sample(rng, 2, tags='food')
            good_1_rate = (rng.integers(1, 11), rng.integers(1, 11))
            good_2_rate = (rng.integers(1, 11), rng.integers(1, 11))
            total_time = rng.choice([5, 10, 15])
            if good_1_rate[0]/good_2_rate[0] == good_1_rate[1]/good_2_rate[1]:
                continue
            if good_1_rate[0] == good_2_rate[0]:
                continue
            if good_1_rate[1] == good_2_rate[1]:
                continue
            yield {
                'type': type,
                'people': people,
                'good_1': my_goods[0],
                'good_2': my_goods[1],
                'good_1_rate': good_1_rate,
                'good_2_rate': good_2_rate,
                'time_units': time_units,
                'total_time': total_time
            }



