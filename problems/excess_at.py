import numpy as np
from econtools.econ.competitive_markets import LinearDemand, LinearSupply, LinearMarket
from econtools.graphs.primitives import Point, Line
from econtools.entities import Good
from econtools.problems.base import GenericProblem, MCQ
from econtools.graphs.axis import Axis
from econtools.math.scaled import Scaled
from itertools import product

class ExcessAt(GenericProblem):
    default_params = {
        # pscale/qscale (price and quantity per grid unit) come from the good
        "good": Good.get("widgets"),
        "price": 8,
        "demand_at": 4,
        "supply_at": 8,
        "equilibrium": (6, 6)
    }
    rpg_topic = "supply-demand"
    rpg_title = "4. Supply and Demand"

    def build(self, rng):
        p = self.params
        good = p['good']
        demand_point = Point(x=p['demand_at'], y=p['price'])
        supply_point = Point(x=p['supply_at'], y=p['price'])
        equilibrium = Point(x=p['equilibrium'][0], y=p['equilibrium'][1])
        demand = LinearDemand.from_points(demand_point, equilibrium, label="D", labelstyle="label", labelshift=0.2)
        supply = LinearSupply.from_points(supply_point, equilibrium, label="S", labelstyle="label", labelshift=0.2)
        market = LinearMarket(demand=demand, supply=supply)
        good = p['good']
        axis = Axis(
            xn=13, yn=13, xscale=good.qscale, yscale=good.pscale, xlab="Quantity", ylab="Price",
            xnumtype='', ynumtype='$', xrot=45, yrot=0 
        )
        axis.add(demand, supply)
        self.add_axis("graph", axis)   # saved as <name>_graph.png by draw_graphs()
        self.demand = demand
        self.supply = supply
        self.market = market
        self.axis = axis
        self.pscale = good.pscale
        self.qscale = good.qscale
        self.price = p['price']
        if p['demand_at'] > p['supply_at']:
            excess_type = "excess demand"
            excess_amount = p['demand_at'] - p['supply_at']
        else:
            excess_type = "excess supply"
            excess_amount = p['supply_at'] - p['demand_at']
        self.sol = {
            "excess_type": excess_type,
            "excess_amount": excess_amount
        }

        # --- setups ---
        setup = f"Supply and demand in the perfectly competitive market for {p['good'].market} is shown in the diagram below."
        setup += "\n\n" + self.latex_image("graph")
        setup += f"\n\nAt a price of {Scaled(p['price'], good.pscale, numtype='$').texify()}, there is \\underline{{\\hspace{{2cm}}}} of \\underline{{\\hspace{{2cm}}}} units."

        online_setup = f"<p>Supply and demand in the perfectly competitive market for {p['good'].market} is shown in the diagram below.</p>"
        online_setup += self.online_image("graph")
        online_setup += f"<p>At a price of {str(Scaled(p['price'], good.pscale, numtype='$'))}, there is ______ of ______ units.</p>"

        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        question = f"Fill in the first blank."
        answer = excess_type
        answers = ["excess demand", "excess supply"]
        solution = answers.index(excess_type)
        mcq = MCQ(question=question, answers=answers, solution=solution, shuffle=False, horz=True, rng=rng)
        self.add_question(question=question, answer=answer, mcq=mcq)

        question = f"Fill in the second blnak."
        answer = excess_amount
        self.add_numeric_question(question=question, answer=answer, rng=rng, scale=good.qscale, numtype='')


    def check_solution(self):
        if self.demand.a <= self.supply.a:
            return False
        if self.demand.a <= self.market.eq['p']:
            return False
        if self.supply.a >= self.market.eq['p']:
            return False
        if self.supply.a < 0:
            return False
        if self.demand.a > 12:
            return False
        if self.sol['excess_amount'] <= 0:
            return False
        return True

    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        for i in range(N_SAMPLES):
            good = Good.sample(rng, tags='market')   # graph scales: good.pscale/qscale per grid unit
            good.qscale = rng.choice([100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 1_000_000])
            price = rng.integers(2, 11)
            eq_x = rng.integers(4, 11)
            eq_y = rng.integers(4, 8)
            if price == eq_y:
                continue
            elif price > eq_y:
                demand_at = rng.integers(1, eq_x)
                supply_at = rng.integers(eq_x+1, 12)
            elif price < eq_y:
                demand_at = rng.integers(eq_x+1, 12)
                supply_at = rng.integers(1, eq_x)
            yield {
                'good': good,
                'price': price,
                'demand_at': demand_at,
                'supply_at': supply_at,
                'equilibrium': (eq_x, eq_y),
            }





    