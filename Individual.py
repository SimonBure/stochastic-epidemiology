
class Individual(object):
    id: int
    remaining_infection_duration: float

    def __init__(self, id: int):
        self.id = id
        self.remaining_infection_duration = 0.

        self.household = None
        self.workplace = None

    def __repr__(self):
        s = f"Individual n°{self.id} - Remaining infection time: {self.remaining_infection_duration}"
        s += f" - Belongs to {str(self.household)} and {str(self.workplace)}"
        return s

    def infection(self, infection_duration: float):
        self.remaining_infection_duration = infection_duration

    def update_remaining_infection_duration(self, time_passed: float):
        self.remaining_infection_duration -= time_passed

    def is_cured(self) -> bool:
        return self.remaining_infection_duration <= 0