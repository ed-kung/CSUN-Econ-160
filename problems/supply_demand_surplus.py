from problems.supply_demand import SupplyDemand


class SupplyDemandSurplus(SupplyDemand):
    """SupplyDemand plus consumer, producer, and total surplus questions."""
    rpg_topic = "consumer-producer-surplus"
    rpg_title = "7. Consumer and Producer Surplus"

    def build(self, rng):
        super().build(rng)   # market, graph, setup, and equilibrium questions
        eq = self.market.eq
        kw = dict(rng=rng, scale=self.pscale * self.qscale, numtype='$')
        self.add_numeric_question("What is the consumer surplus in the market?", eq['CS'], **kw)
        self.add_numeric_question("What is the producer surplus in the market?", eq['PS'], **kw)
        self.add_numeric_question("What is the total surplus in the market?", eq['CS'] + eq['PS'], **kw)
