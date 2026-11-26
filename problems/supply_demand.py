import numpy as np
from econtools.econ.competitive_markets import LinearDemand, LinearSupply, LinearMarket
from econtools.graphs.primitives import Point, Line
from econtools.entities import Good
from econtools.problems.base import GenericProblem
from econtools.graphs.axis import Axis

class SupplyDemand(GenericProblem):
    default_params = {
        # pscale/qscale (price and quantity per grid unit) come from the good
        "good": Good.get("widget"),
        "demand_point": (0, 12),
        "supply_point": (0, 0),
        "equilibrium": (6, 6),
        "pmax": 13,
        "qmax": 13
    }
    rpg_topic = "supply-demand"
    rpg_title = "4. Supply and Demand"

    def build(self, rng):
        p = self.params
        demand_point = Point(x=p['demand_point'][0], y=p['demand_point'][1])
        supply_point = Point(x=p['supply_point'][0], y=p['supply_point'][1])
        equilibrium = Point(x=p['equilibrium'][0], y=p['equilibrium'][1])
        demand = LinearDemand.from_points(demand_point, equilibrium, label="D", labelstyle="label", labelshift=0.2)
        supply = LinearSupply.from_points(supply_point, equilibrium, label="S", labelstyle="label", labelshift=0.2)
        demand_xg = np.arange(0, min(demand.eval_at_p(1)+0.1, 12), 0.1)
        supply_xg = np.arange(0, min(supply.eval_at_p(p['pmax']-1)+0.1, 12), 0.1)
        demand.line.plot_x = demand_xg
        supply.line.plot_x = supply_xg
        market = LinearMarket(demand=demand, supply=supply)
        good = p['good']
        axis = Axis(
            xn=p['qmax'], yn=p['pmax'], xscale=good.qscale, yscale=good.pscale, xlab="Quantity", ylab="Price",
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
        setup = f"Supply and demand in the perfectly competitive market for {p['good'].plural} is shown in the diagram below."
        setup += "\n\n" + self.latex_image("graph")
        online_setup = f"<p>Supply and demand in the perfectly competitive market for {p['good'].plural} is shown in the diagram below.</p>"
        online_setup += self.online_image("graph")

        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        eq = self.market.eq
        self.add_numeric_question("What is the equilibrium price in the market?", eq['p'],
                                  rng=rng, scale=self.pscale, numtype='$')
        self.add_numeric_question("What is the equilibrium quantity in the market?", eq['q'],
                                  rng=rng, scale=self.qscale, numtype='')
        self.add_numeric_question("What is the total volume of transactions in the market?", eq['p'] * eq['q'],
                                  rng=rng, scale=self.pscale * self.qscale, numtype='$')

    def check_solution(self):
        if self.demand.a <= self.supply.a:
            return False
        if self.demand.a <= self.market.eq['p']:
            return False
        if self.supply.a >= self.market.eq['p']:
            return False
        return True
    
    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        for i in range(N_SAMPLES):
            good = Good.sample(rng, tags='market')   # graph scales: good.pscale/qscale per grid unit
            eq_x = rng.integers(4, 11)
            eq_y = rng.integers(4, 8)
            demand_a = rng.integers(eq_y+1, 13)
            supply_a = rng.integers(0, eq_y)
            yield {
                'good': good,
                'demand_point': (0, demand_a),
                'supply_point': (0, supply_a),
                'equilibrium': (eq_x, eq_y),
                'pmax': 13,
                'qmax': 13
            }
