import numpy as np
from econtools.econ.competitive_markets import LinearDemand, LinearSupply, LinearMarket
from econtools.graphs.primitives import Point, Line
from econtools.entities import Good
from econtools.problems.base import GenericProblem
from econtools.graphs.axis import Axis

class PSChange(GenericProblem):
    default_params = {
        # pscale/qscale (price and quantity per grid unit) come from the good
        "good": Good.get("widgets"),
        "equilibrium": (6, 6),
        "new_supply_point": (8, 8),
        "old_demand_point": (0, 12)
    }
    rpg_topic = "consumer-producer-surplus"
    rpg_title = "7. Consumer and Producer Surplus"

    def build(self, rng):
        p = self.params
        equilibrium = Point(x=p['equilibrium'][0], y=p['equilibrium'][1])
        new_supply_point = Point(x=p['new_supply_point'][0], y=p['new_supply_point'][1])
        old_demand_point = Point(x=p['old_demand_point'][0], y=p['old_demand_point'][1])

        supply = LinearSupply.from_points(new_supply_point, equilibrium, label="S", labelstyle="label", labelshift=0.2)
        demand1 = LinearDemand.from_points(old_demand_point, equilibrium, label="D1", labelstyle="label", labelshift=0.2)
        demand2 = LinearDemand.from_point_slope(point=new_supply_point, slope=-demand1.b, label="D2", labelstyle="label", labelshift=0.2, color='red')
        market1 = LinearMarket(demand=demand1, supply=supply)
        market2 = LinearMarket(demand=demand2, supply=supply)

        PS_change = 0.5 * (new_supply_point.y - equilibrium.y) * (new_supply_point.x + equilibrium.x)

        good = p['good']
        axis = Axis(
            xn=13, yn=13, xscale=good.qscale, yscale=good.pscale, xlab="Quantity", ylab="Price",
            xnumtype='', ynumtype='$', xrot=45, yrot=0 
        )
        axis.add(demand1, demand2, supply)
        self.add_axis("graph", axis)   # saved as <name>_graph.png by draw_graphs()
        self.demand1 = demand1
        self.demand2 = demand2
        self.supply = supply
        self.market1 = market1
        self.market2 = market2
        self.axis = axis
        self.pscale = good.pscale
        self.qscale = good.qscale
        self.sol = {
            'PS_change': PS_change
        }

        # --- setups ---
        setup = f"Supply and demand in the perfectly competitive market for {p['good'].market} is shown in the diagram below."
        setup += "\n\n" + self.latex_image("graph")
        setup += f"\n\nOne day, the demand curve changes from D1 to D2."

        online_setup = f"<p>Supply and demand in the perfectly competitive market for {p['good'].market} is shown in the diagram below.</p>"
        online_setup += self.online_image("graph")
        online_setup += f"<p>One day, the demand curve changes from D1 to D2.</p>"

        self.add_setup(setup=setup, online_setup=online_setup)

        # --- questions ---
        q = "Calculate the change in producer surplus as demand moves from D1 to D2."
        self.add_numeric_question(q, answer=PS_change, rng=rng, scale=self.pscale*self.qscale, numtype='$')

    def check_solution(self):
        if self.demand1.a <= self.supply.a:
            return False
        if self.demand2.a <= self.supply.a:
            return False
        if self.demand1.a == self.demand2.a:
            return False
        if self.demand1.b <= 0:
            return False
        if self.demand2.b <= 0:
            return False
        if self.demand1.a > 12:
            return False
        if self.supply.a < 0:
            return False
        return True
    
    @classmethod
    def candidate_params(cls, rng):
        N_SAMPLES = 300
        for i in range(N_SAMPLES):
            good = Good.sample(rng, tags='market')   # graph scales: good.pscale/qscale per grid unit
            good.qscale = rng.choice([100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 1_000_000])
            eq_x = rng.integers(4, 9)
            eq_y = rng.integers(4, 8)
            old_demand_point = (0, rng.integers(eq_y+1, 13))

            flip = rng.integers(0, 2)
            if flip == 0:
                new_supply_point = (rng.integers(2, eq_x), rng.integers(2, eq_y))
            else:
                new_supply_point = (rng.integers(eq_x+1, 11), rng.integers(eq_y+1, 11))

            equilibrium = (eq_x, eq_y)

            yield {
                'good': good,
                'equilibrium': equilibrium,
                'new_supply_point': new_supply_point,
                'old_demand_point': old_demand_point
            }