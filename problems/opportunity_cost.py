import numpy as np
from econtools.entities import Good, Person
from econtools.problems.base import GenericProblem

class OpportunityCost(GenericProblem):
    default_params = {
        'person': Person.get('Anna'),
        'good_1': Good.get('popsicles'),
        'good_2': Good.get('ice cream'),
        'good_1_rate': 6,
        'good_2_rate': 5
    }
    rpg_topic = "specialization-trade"
    rpg_title = "3. Specialization and Trade"

    def build(self, rng):
        p = self.params
        name = p['person'].name
        good_1 = p['good_1']
        good_2 = p['good_2']
        good_1_rate = p['good_1_rate']
        good_2_rate = p['good_2_rate']
        opportunity_cost_good_1 = good_2_rate / good_1_rate
        opportunity_cost_good_2 = good_1_rate / good_2_rate
        self.sol = {
            'opportunity_cost_good_1': opportunity_cost_good_1,
            'opportunity_cost_good_2': opportunity_cost_good_2
        }

        # ---- setups ----
        setup = f"{name} can produce {good_1.market} at a rate of {good_1.amount(good_1_rate, full=False)} per hour or {good_2.market} at a rate of {good_2.amount(good_2_rate, full=False)} per hour."
        self.add_setup(setup=setup)

        # ---- questions ----
        self.add_numeric_question(
            f"What is {name}'s opportunity cost of producing {good_1.market}, in {good_2.units} foregone per {good_1.unit} produced?",
            self.sol['opportunity_cost_good_1'], rng=rng
        )
        self.add_numeric_question(
            f"What is {name}'s opportunity cost of producing {good_2.market}, in {good_1.units} foregone per {good_2.unit} produced?",
            self.sol['opportunity_cost_good_2'], rng=rng
        )

    def check_solution(self):
        if self.sol['opportunity_cost_good_1'] <= 0:
            return False
        if self.sol['opportunity_cost_good_2'] <= 0:
            return False
        return True
    
    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        for i in range(N_SAMPLES):
            person = Person.sample(rng)
            good_1, good_2 = Good.sample(rng, 2, tags='food')
            good_1_rate = rng.integers(1, 11)
            good_2_rate = rng.integers(1, 11)
            yield {
                'person': person,
                'good_1': good_1,
                'good_2': good_2,
                'good_1_rate': good_1_rate,
                'good_2_rate': good_2_rate
            }
