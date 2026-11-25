import numpy as np
from econtools.econ.competitive_markets import LinearDemand, LinearSupply, LinearMarket
from econtools.graphs.primitives import Point, Line
from econtools.problems.base import GenericProblem
from econtools.graphs.axis import Axis

class SupplyDemand(GenericProblem):
    default_params = {
        "singular": "widget",
        "plural": "widgets",
        "demand_point": (0, 12),
        "supply_point": (0, 0),
        "equilibrium": (6, 6),
        "pscale": 5,
        "qscale": 1000,
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
        axis = Axis(
            xn=p['qmax'], yn=p['pmax'], xscale=p['qscale'], yscale=p['pscale'], xlab="Quantity", ylab="Price",
            xnumtype='', ynumtype='$', xrot=45, yrot=0 
        )
        axis.add(demand, supply)
        self.add_axis("graph", axis)   # saved as <name>_graph.png by draw_graphs()
        self.demand = demand
        self.supply = supply
        self.market = market
        self.axis = axis
        self.pscale = p['pscale']
        self.qscale = p['qscale']

        # --- setups ---
        setup = f"Supply and demand in the perfectly competitive market for {p['plural']} is shown in the diagram below."
        setup += "\n\n" + self.latex_image("graph")
        online_setup = f"<p>Supply and demand in the perfectly competitive market for {p['plural']} is shown in the diagram below.</p>"
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
        names = [
            ('widget', 'widgets'),
            ('coffee', 'coffee'),
            ('robot', 'robots'),
            ('corn', 'corn'),
            ('doodad', 'doodads'),
            ('bike', 'bikes'),
            ('USB stick', 'USB sticks')
        ]
        for i in range(N_SAMPLES):
            name = rng.choice(names)
            singular = name[0]
            plural = name[1]
            if singular == 'coffee':
                pscale = 5
            elif singular == 'corn':
                pscale = rng.choice([1, 2, 5, 10])
            elif singular == 'bike':
                pscale = 25
            elif singular == 'USB stick':
                pscale = 2
            else:
                pscale = rng.choice([1, 2, 5, 10, 20, 50])
            qscale = rng.choice([1000, 5000, 10_000, 50_000, 1_000_000])
            eq_x = rng.integers(4, 11)
            eq_y = rng.integers(4, 8)
            demand_a = rng.integers(eq_y+1, 13)
            supply_a = rng.integers(0, eq_y)
            yield {
                'singular': singular,
                'plural': plural,
                'demand_point': (0, demand_a),
                'supply_point': (0, supply_a),
                'equilibrium': (eq_x, eq_y),
                'pscale': pscale,
                'qscale': qscale,
                'pmax': 13,
                'qmax': 13
            }
