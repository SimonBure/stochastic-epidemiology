import numpy as np
from Individual import Individual

class Epidemic:
    population_size: int
    individuals: [Individual]
    susceptible: int
    infected: int
    recovered: int

    global_infection_rate: float
    households_infection_rate: float
    workplaces_infection_rate: float

    mean_infection_time: float
    deviation_infection_rate: float

    time: float
    max_time: float


    def __init__(self, population_size: int, individuals: [Individual], global_infection_rate: float,
                 mean_infection_time: float, deviation_infection_rate: float, max_time: float):
        self.population_size = population_size
        self.individuals = individuals
        self.susceptible = self.population_size
        self.infected = 0
        self.recovered = 0

        self.global_infection_rate = global_infection_rate

        self.mean_infection_time = mean_infection_time
        self.deviation_infection_rate = deviation_infection_rate

        self.time = 0
        self.max_time = max_time

    def generate_random_infection_time(self) -> float:
        return np.random.normal(self.mean_infection_time, self.deviation_infection_rate)

    def global_infection(self):
        infected = np.random.choice(self.individuals)
        infected.infection(self.generate_random_infection_time())
