class Individual(object):
    remaining_infection_time: float
    is_infected: bool
    is_recovered: bool

    def __init__(self):
        self.is_infected = False
        self.is_recovered = False
        self.remaining_infection_time = 0.