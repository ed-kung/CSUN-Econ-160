import numpy as np
from econtools.econ.competitive_markets import LinearDemand, LinearSupply, LinearMarket
from econtools.graphs.primitives import Point, Line
from econtools.entities import Good
from econtools.problems.base import GenericProblem, MCQ
from econtools.graphs.axis import Axis
from econtools.math.scaled import Scaled
from itertools import product

class ElasticityGraph(GenericProblem):
    default_params = {
        # pscale/qscale (price and quantity per grid unit) come from the good
        "good": Good.get("widgets"),
        "demand_point_1": (4, 8),
        "demand_point_2": (8, 4),
        "supply_point_1": (4, 4),
        "supply_point_2": (8, 8)
    }
    rpg_topic = "elasticity"
    rpg_title = "6. Elasticity"

    def build(self, rng):
        p = self.params
        good = p['good']

        demand_point_1 = Point(x=p['demand_point_1'][0], y=p['demand_point_1'][1])
        demand_point_2 = Point(x=p['demand_point_2'][0], y=p['demand_point_2'][1])
        supply_point_1 = Point(x=p['supply_point_1'][0], y=p['supply_point_1'][1])
        supply_point_2 = Point(x=p['supply_point_2'][0], y=p['supply_point_2'][1])
        demand = LinearDemand.from_points(demand_point_1, demand_point_2, label="D", labelstyle="label", labelshift=0.2)
        supply = LinearSupply.from_points(supply_point_1, supply_point_2, label="S", labelstyle="label", labelshift=0.2)
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

        # --- setups ---
        setup = f"Supply and demand in the perfectly competitive market for {p['good'].market} is shown in the diagram below."
        setup += "\n\n" + self.latex_image("graph")

        online_setup = f"<p>Supply and demand in the perfectly competitive market for {p['good'].market} is shown in the diagram below.</p>"
        online_setup += self.online_image("graph")

        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        p1 = demand_point_1.y
        p2 = demand_point_2.y
        q1 = demand_point_1.x
        q2 = demand_point_2.x
        elast = (q2 - q1)/(0.5*(q1+q2)) / ((p2 - p1)/(0.5*(p1+p2)))
        question = f"Calculate the price elasticity of demand as price goes from {Scaled(p1, good.pscale, numtype='$').texify()} to {Scaled(p2, good.pscale, numtype='$').texify()}."
        online_question = f"Calculate the price elasticity of demand as price goes from {str(Scaled(p1, good.pscale, numtype='$'))} to {str(Scaled(p2, good.pscale, numtype='$'))}."
        answer = elast
        self.add_numeric_question(question=question, online_question=online_question, answer=answer, rng=rng, scale=1, numtype='')

        p1 = supply_point_1.y
        p2 = supply_point_2.y
        q1 = supply_point_1.x
        q2 = supply_point_2.x
        elast = (q2 - q1)/(0.5*(q1+q2)) / ((p2 - p1)/(0.5*(p1+p2)))
        question = f"Calculate the price elasticity of supply as price goes from {Scaled(p1, good.pscale, numtype='$').texify()} to {Scaled(p2, good.pscale, numtype='$').texify()}."
        online_question = f"Calculate the price elasticity of supply as price goes from {str(Scaled(p1, good.pscale, numtype='$'))} to {str(Scaled(p2, good.pscale, numtype='$'))}."
        answer = elast
        self.add_numeric_question(question=question, online_question=online_question, answer=answer, rng=rng, scale=1, numtype='')

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
        return True

    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        for i in range(N_SAMPLES):
            good = Good.sample(rng, tags='market')   # graph scales: good.pscale/qscale per grid unit
            good.qscale = rng.choice([100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 1_000_000])
            demand_point_1 = (rng.integers(2, 7), rng.integers(5, 10))
            demand_point_2 = (rng.integers(demand_point_1[0]+1, 12), rng.integers(1, demand_point_1[1]))
            supply_point_1 = (rng.integers(2, 6), rng.integers(2, 6))
            supply_point_2 = (rng.integers(supply_point_1[0]+1, 12), rng.integers(supply_point_1[1]+1, 12))

            demand_points = [demand_point_1, demand_point_2]
            supply_points = [supply_point_1, supply_point_2]

            demand_idx = rng.integers(0, 2)
            supply_idx = rng.integers(0, 2)

            yield {
                'good': good,
                'demand_point_1': demand_points[demand_idx],
                'demand_point_2': demand_points[1-demand_idx],
                'supply_point_1': supply_points[supply_idx],
                'supply_point_2': supply_points[1-supply_idx],
            }


    