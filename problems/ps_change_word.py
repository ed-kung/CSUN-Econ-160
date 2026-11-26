from econtools.math.scaled import Scaled

from problems.ps_change import PSChange


class PSChangeWord(PSChange):
    """PSChange as a word problem: the old and new equilibria are stated in the text, no graph."""

    def build(self, rng):
        super().build(rng)   # curves, solution, and check_solution inputs
        p = self.params
        good = p['good']
        (q1, p1), (q2, p2) = p['equilibrium'], p['new_supply_point']
        price1, price2 = Scaled(p1, good.pscale, numtype='$'), Scaled(p2, good.pscale, numtype='$')
        qty1, qty2 = Scaled(q1, good.qscale), Scaled(q2, good.qscale)
        direction = "increases" if q2 > q1 else "decreases"

        # replace the graph setup and question
        self.axes = {}
        self.setup_list = []
        self.question_list = []

        setup = (f"The perfectly competitive market for {good.market} is in equilibrium, "
                 f"with an equilibrium price of {price1.texify()} per {good.unit} and an equilibrium "
                 f"quantity traded of {qty1.texify()} {good.units}. One day, demand {direction}, "
                 f"and the new equilibrium price is {price2.texify()} per {good.unit} and the new "
                 f"quantity traded is {qty2.texify()} {good.units}.")
        online_setup = (f"<p>The perfectly competitive market for {good.market} is in equilibrium, "
                        f"with an equilibrium price of {price1} per {good.unit} and an equilibrium "
                        f"quantity traded of {qty1} {good.units}. One day, demand {direction}, "
                        f"and the new equilibrium price is {price2} per {good.unit} and the new "
                        f"quantity traded is {qty2} {good.units}.</p>")
        self.add_setup(setup=setup, online_setup=online_setup)

        q = "Calculate the change in producer surplus."
        self.add_numeric_question(q, answer=self.sol['PS_change'], rng=rng,
                                  scale=self.pscale*self.qscale, numtype='$')
