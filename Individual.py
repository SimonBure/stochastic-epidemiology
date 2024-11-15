
class Individual(object):
    id: int
    remaining_infection_duration: float
    is_infected: bool
    is_recovered: bool
    household: object
    workplace: object

    def __init__(self, id: int):
        self.id = id
        self.is_infected = False
        self.is_recovered = False
        self.remaining_infection_duration = 0.

    def __repr__(self):
        s = f"Individual n°{self.id} - Infected? {self.is_infected} - "
        s += f"Remaining infection time: {self.remaining_infection_duration}) - Recovered? {self.is_recovered}"
        s += f" - Belongs to {str(self.household)} and {str(self.workplace)}"
        return s

    def infection(self, infection_duration: float):
        self.is_infected = True
        self.remaining_infection_duration = infection_duration
        self.household.remove_susceptible(self)
        self.workplace.remove_susceptible(self)

    def update_infection(self, time_passed: float):
        self.remaining_infection_duration -= time_passed
        if self.remaining_infection_duration <= 0:
            self.healing()

    def healing(self):
        self.is_infected = False
        self.is_recovered = True