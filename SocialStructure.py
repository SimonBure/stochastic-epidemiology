import abc
import numpy as np
from Cluster import Cluster, Household, Workplace


class SocialStructure(abc.ABC):
    infection_rate: float
    clusters: list[Cluster] = []

    def __init__(self, infection_rate: float):
        self.infection_rate = infection_rate

    def __repr__(self):
        s = ""
        for c in self.clusters:
            s += str(c) + "\n"

        return s

    def get_susceptible(self) -> int:
        return sum(c.susceptible for c in self.clusters)

    def get_infected(self) -> int:
        return sum([c.infected_nb for c in self.clusters])

    def get_recovered(self) -> int:
        return sum(c.recovered_nb for c in self.clusters)

    def get_random_cluster(self) -> Cluster:
        return np.random.choice(self.clusters)

    def get_infected_clusters(self) -> list[Cluster]:
        infected_clusters = []
        for c in self.clusters:
            if c.infected_nb > 0:
                infected_clusters.append(c)

        return infected_clusters

    def get_random_infected_cluster(self, infected_clusters: list[Cluster], clusters_infection_rates=None) -> Cluster:
        return np.random.choice(infected_clusters, p=clusters_infection_rates)

    def get_infection_rates(self, infected_clusters: list[Cluster]) -> list[float]:
        return [self.infection_rate * c.susceptible_nb * c.infected_nb for c in infected_clusters]

# TODO make the H and W iterable
class Households(SocialStructure):
    def __init__(self, infection_rate: float, population_size: int):
        super().__init__(infection_rate)
        self.clusters = []

        households_sizes = [i for i in range(1, 7)]
        households_sizes_frequencies = np.loadtxt("data/insee_households.csv", delimiter=",")

        pop = 0
        id = 0
        while pop < population_size:
            random_household_size = np.random.choice(households_sizes,p=households_sizes_frequencies)
            while pop + random_household_size > population_size:
                random_household_size = np.random.choice(households_sizes, p=households_sizes_frequencies)
            self.clusters.append(Household(id, random_household_size, self.infection_rate))
            id += 1
            pop += random_household_size


class Workplaces(SocialStructure):
    def __init__(self, infection_rate: float, population_size: int):
        super().__init__(infection_rate)
        self.clusters = []

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
