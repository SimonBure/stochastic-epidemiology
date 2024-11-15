import abc
import numpy as np
from Cluster import Cluster, Household, Workplace


class SocialStructure(abc.ABC):
    infection_rate: float
    clusters: list[Cluster] = []

    def __init__(self, infection_rate: float):
        self.infection_rate = infection_rate

    def __repr__(self):
        s = f""

        return s

    def get_susceptible(self) -> int:
        return sum(c.susceptible for c in self.clusters)

    def get_infected(self) -> int:
        return sum([c.infected_nb for c in self.clusters])

    def get_recovered(self) -> int:
        return sum(c.recovered_nb for c in self.clusters)

    def get_random_cluster(self) -> Cluster:
        return np.random.choice(self.clusters)

# TODO make the H and W iterable
class Households(SocialStructure):
    def __init__(self, infection_rate: float, population_size: int):
        super().__init__(infection_rate)
        households_sizes = [i for i in range(1, 7)]
        households_sizes_frequencies = np.loadtxt("data/insee_households.csv", delimiter=",")

        pop = 0
        id = 0
        while pop < population_size:
            random_household_size = np.random.choice(households_sizes, None, replace=True, p=households_sizes_frequencies)
            while pop + random_household_size > population_size:
                random_household_size = np.random.choice(households_sizes, None, replace=True, p=households_sizes_frequencies)
            self.clusters.append(Household(id, random_household_size, self.infection_rate))
            id += 1
            pop += random_household_size


class Workplaces(SocialStructure):
    def __init__(self, infection_rate: float, population_size: int):
        super().__init__(infection_rate)
        workplaces_sizes = [i for i in range(1, 51)]
        workplaces_sizes_frequencies = np.loadtxt("data/insee_workplaces.csv", delimiter=",")

        pop = 0
        id = 0
        while pop < population_size:
            random_workplace_size = np.random.choice(workplaces_sizes, None, replace=True, p=workplaces_sizes_frequencies)
            while pop + random_workplace_size > population_size:
                random_workplace_size = np.random.choice(workplaces_sizes, None, replace=True, p=workplaces_sizes_frequencies)
            self.clusters.append(Workplace(id, random_workplace_size, self.infection_rate))
            id += 1
            pop += random_workplace_size
