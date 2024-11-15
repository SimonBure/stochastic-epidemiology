import abc
from Individual import Individual

class Cluster(abc.ABC):
    id: int
    size: int
    susceptible_nb: int
    infection_rate: float
    individuals_inside: list[Individual]

    def __init__(self, id: int, size: int, infection_rate: float):
        self.id = id
        self.size = size
        self.susceptible_nb = self.size
        self.infection_rate = infection_rate
        self.individuals_inside = [Individual() for _ in range(size)]

    def __repr__(self):
        return f"n°{self.id} - Size: {self.size} - Susceptible: {self.susceptible_nb}"


class Household(Cluster):
    def __repr__(self):
        return "Household " + super().__repr__()


class Workplace(Cluster):
    def __repr__(self):
        return "Workplace " + super().__repr__()