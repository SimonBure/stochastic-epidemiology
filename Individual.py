
class Individual(object):
    id: int
    remaining_infection_time: float
    is_infected: bool
    is_recovered: bool
    household: object
    workplace: object

    def __init__(self, id: int):
        self.id = id
        self.is_infected = False
        self.is_recovered = False
        self.remaining_infection_time = 0.

    def __repr__(self):
        s = f"Individual n°{self.id} - Infected? {self.is_infected} - "
        s += f"Remaining infection time: {self.remaining_infection_time}) - Recovered? {self.is_recovered}"
        s += f" - Belongs to {str(self.household)} and {str(self.workplace)}"
        return s