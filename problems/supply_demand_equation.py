import numpy as np
from econtools.entities import Good
from econtools.problems.base import GenericProblem
from econtools.math.equations import PolyEq

class SupplyDemandEquation(GenericProblem):
    # qd = demand_intercept + demand_slope*p
    # qs = supply_slope*p + supply_intercept
    # equilibrium_price = (demand_intercept - supply_intercept) / (supply_slope - demand_slope)

    default_params = {
        "good": Good.get("widgets"),
        "demand_intercept": 100,
        "demand_slope": -1,
        "supply_intercept": 0,
        "supply_slope": 1
    }
    rpg_topic = "supply-demand"
    rpg_title = "4. Supply and Demand"

    def build(self, rng):
        p = self.params
        demand_intercept = p['demand_intercept']
        demand_slope = p['demand_slope']
        supply_intercept = p['supply_intercept']
        supply_slope = p['supply_slope']
        equilibrium_price = (demand_intercept - supply_intercept) / (supply_slope - demand_slope)
        equilibrium_quantity = demand_intercept + demand_slope*equilibrium_price
        demand_eq = PolyEq([demand_intercept, demand_slope], 'p', [0, 1])
        supply_eq = PolyEq([supply_slope, supply_intercept], 'p', [1, 0])
        self.sol = {
            'equilibrium_price': equilibrium_price,
            'equilibrium_quantity': equilibrium_quantity
        }

        # ---- setups ----
        setup = f"Demand and supply in the market for {p['good'].market} are given by the following equations:\n\n"
        setup += f"\\begin{{align}}\n"
        setup += f"q_d &= {demand_eq.print()} \\\\ \n"
        setup += f"q_s &= {supply_eq.print()} \n"
        setup += f"\\end{{align}}\n\n"

        online_setup = f"<p>Demand and supply in the market for {p['good'].market} are given by the following equations:</p>\n\n"
        online_setup += f"$$\\begin{{align}}\n"
        online_setup += f"q_d &= {demand_eq.print()} \\\\ \n"
        online_setup += f"q_s &= {supply_eq.print()} \n"
        online_setup += f"\\end{{align}}$$\n\n"

        self.add_setup(setup=setup, online_setup=online_setup)
        
        # ---- questions ----
        self.add_numeric_question("What is the equilibrium price in this market?", self.sol['equilibrium_price'], rng=rng, scale=1, numtype='')
        self.add_numeric_question("What is the equilibrium quantity in this market?", self.sol['equilibrium_quantity'], rng=rng, scale=1, numtype='')

    def check_solution(self):
        if self.sol['equilibrium_price'] <= 0:
            return False
        if self.sol['equilibrium_quantity'] <= 0:
            return False
        return True
    
    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        for i in range(N_SAMPLES):
            good = Good.sample(rng, tags='market')
            demand_intercept = rng.integers(10, 101)
            demand_slope = rng.integers(-10, 0)
            supply_intercept = rng.integers(-20, demand_intercept-10+1)
            supply_slope = rng.integers(1, 11)
            yield {
                'good': good,
                'demand_intercept': demand_intercept,
                'demand_slope': demand_slope,
                'supply_intercept': supply_intercept,
                'supply_slope': supply_slope
            }


