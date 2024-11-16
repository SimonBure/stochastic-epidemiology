import abc
import numpy as np
from Individual import Individual

class Cluster(abc.ABC):
    id: int
    size: int
    susceptible: list[Individual]
    susceptible_nb: int
    infected_nb: int
    recovered_nb: int
    infection_proba: float
    individuals_inside: list[Individual]

    def __init__(self, id: int, size: int, infection_rate: float):
        self.id = id
        self.size = size
        self.susceptible = []
        self.susceptible_nb = self.size
        self.infected_nb = 0
        self.recovered_nb = 0
        self.infection_proba = infection_rate

    def __repr__(self):
        s = f"n°{self.id} - Size: {self.size} - Susceptible: {len(self.susceptible)} - Infected: {self.infected_nb}"
        s += f" Recovered: {self.recovered_nb}"

        return s

    def get_random_susceptible(self) -> Individual:
        return np.random.choice(self.susceptible)

    def add_individual(self, individual: Individual):
        self.susceptible.append(individual)

    def remove_susceptible(self, infected: Individual):
        self.susceptible.remove(infected)

    def is_full(self) -> bool:
        return self.size == len(self.susceptible)

    def update_after_infection(self):
        self.susceptible_nb -= 1
        self.infected_nb += 1

    def healing_event(self):
        self.infected_nb -= 1
        self.susceptible += 1


class Household(Cluster):
    def __repr__(self):
        return "Household " + super().__repr__()


class Workplace(Cluster):
    def __repr__(self):
        return "Workplace " + super().__repr__()