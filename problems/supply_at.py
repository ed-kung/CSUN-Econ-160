import numpy as np
from econtools.econ.competitive_markets import LinearDemand, LinearSupply, LinearMarket
from econtools.graphs.primitives import Point, Line
from econtools.entities import Good
from econtools.problems.base import GenericProblem
from econtools.graphs.axis import Axis
from econtools.math.scaled import Scaled
from itertools import product

class SupplyAt(GenericProblem):
    default_params = {
        # pscale/qscale (price and quantity per grid unit) come from the good
        "good": Good.get("widgets"),
        "point1": (2, 10),
        "point2": (10, 2)
    }
    rpg_topic = "supply-demand"
    rpg_title = "4. Supply and Demand"

    def build(self, rng):
        p = self.params
        good = p['good']
        point1 = Point(x=p['point1'][0], y=p['point1'][1])
        point2 = Point(x=p['point2'][0], y=p['point2'][1])
        supply = LinearSupply.from_points(point1, point2, label="S", labelstyle="label", labelshift=0.2)
        supply_xg = np.arange(0, min(supply.eval_at_p(13-1)+0.1, 12), 0.1)
        supply.line.plot_x = supply_xg
        axis = Axis(
            xn=13, yn=13, xscale=good.qscale, yscale=good.pscale, xlab="Quantity", ylab="Price",
            xnumtype='', ynumtype='$', xrot=45, yrot=0 
        )
        axis.add(supply)
        self.add_axis("graph", axis)   # saved as <name>_graph.png by draw_graphs()
        self.supply = supply
        self.axis = axis
        self.point1 = point1
        self.point2 = point2
        self.good = good
        self.pscale = good.pscale
        self.qscale = good.qscale
        
        # ---- setups ----
        setup = f"The market supply curve for {p['good'].market} is shown in the diagram below."
        setup += "\n\n" + self.latex_image("graph")
        online_setup = f"<p>The market supply curve for {p['good'].market} is shown in the diagram below.</p>"
        online_setup += self.online_image("graph")
        self.add_setup(setup=setup, online_setup=online_setup)

        # ---- questions ----
        p1 = Scaled(point1.y, good.pscale, numtype='$')
        question = f"At a price of {p1.texify()}, what is the quantity supplied?"
        online_question = f"At a price of {str(p1)}, what is the quantity supplied?"
        ans = point1.x
        self.add_numeric_question(question=question, online_question=online_question, answer=ans, rng=rng, scale=good.qscale, numtype='')

        q2 = Scaled(point2.x, good.qscale, numtype='')
        question = f"At what price would quantity supplied be equal to {str(q2)}?"
        ans = point2.y
        self.add_numeric_question(question=question, answer=ans, rng=rng, scale=good.pscale, numtype='$')

        question = f"Suppose {str(q2)} units are being produced. What is the marginal cost of the last unit produced?"
        ans = point2.y
        self.add_numeric_question(question=question, answer=ans, rng=rng, scale=good.pscale, numtype='$')

    def check_solution(self):
        if self.supply.a < 0:
            return False
        return True

    @classmethod
    def candidate_params(cls, rng):
        for point1_x, point1_y in product(range(2,9), range(2,9)):
            for point2_x, point2_y in product(range(point1_x+1,12), range(point1_y+1,12)):
                good = Good.sample(rng, tags='market')
                good.qscale = rng.choice([100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 1_000_000])
                yield {
                    'good': good,
                    'point1': (point1_x, point1_y),
                    'point2': (point2_x, point2_y)
                }
                yield {
                    'good': good,
                    'point1': (point2_x, point2_y),
                    'point2': (point1_x, point1_y)
                }





    