import numpy as np
from econtools.problems.base import GenericProblem

class OpportunityCost(GenericProblem):
    default_params = {
        'name': 'Anna',
        'good_1': ('popsicle', 'popsicles'),
        'good_2': ('ice cream scoop', 'ice cream scoops'),
        'good_1_rate': 6,
        'good_2_rate': 5
    }
    rpg_topic = "specialization-trade"
    rpg_title = "3. Specialization and Trade"

    def build(self, rng):
        p = self.params
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
        setup = f"{p['name']} can produce {good_1[1]} at a rate of {good_1_rate} per hour or {good_2[1]} at a rate of {good_2_rate} per hour."
        self.add_setup(setup=setup)

        # ---- questions ----
        self.add_numeric_question(
            f"What is {p['name']}'s opportunity cost of producing {good_1[1]}, in units of {good_2[1]} foregone per unit of {good_1[1]} produced?",
            self.sol['opportunity_cost_good_1'], rng=rng
        )
        self.add_numeric_question(
            f"What is {p['name']}'s opportunity cost of producing {good_2[1]}, in units of {good_1[1]} foregone per unit of {good_2[1]} produced?",
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
        names = ['Anna', 'Bob', 'Charlie', 'Diana', 'Ethan', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia']
        goods = [
            ('popsicle', 'popsicles'),
            ('ice cream scoop', 'ice cream scoops'),
            ('sandwich', 'sandwiches'),
            ('cookie', 'cookies'),
            ('cake', 'cakes'),
            ('pizza', 'pizzas'),
            ('hamburger', 'hamburgers')
        ]
        for i in range(N_SAMPLES):
            name = rng.choice(names)
            goods = rng.choice(goods, size=2, replace=False)
            good_1 = goods[0]
            good_2 = goods[1]
            good_1_rate = rng.integers(1, 11)
            good_2_rate = rng.integers(1, 11)
            yield {
                'name': name,
                'good_1': good_1,
                'good_2': good_2,
                'good_1_rate': good_1_rate,
                'good_2_rate': good_2_rate
            }
