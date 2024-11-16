
class Individual(object):
    id: int
    remaining_infection_duration: float
    household: object
    workplace: object

    def __init__(self, id: int):
        self.id = id
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
        self.household.update_after_infection()

        self.workplace.remove_susceptible(self)
        self.workplace.update_after_infection()

    def update_remaining_infection_duration(self, time_passed: float):
        self.remaining_infection_duration -= time_passed

    def is_cured(self) -> bool:
        return self.remaining_infection_duration <= 0