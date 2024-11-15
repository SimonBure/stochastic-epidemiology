import numpy as np
import random
import matplotlib.pyplot as plt
from Cluster import Household, Workplace
from Individual import Individual


def create_households_list(population_size: int, households_infection_rate: float) -> list[Household]:
    households_sizes = [i for i in range(1, 7)]
    households_sizes_frequencies = np.loadtxt("data/insee_households.csv", delimiter=",")
    households_list = []

    pop = 0
    id = 0
    while pop < population_size:
        random_household_size = generate_random_cluster_size(households_sizes, households_sizes_frequencies)
        while pop + random_household_size > population_size:
            random_household_size = generate_random_cluster_size(households_sizes, households_sizes_frequencies)
        households_list.append(Household(id, random_household_size, households_infection_rate))
        id += 1
        pop += random_household_size

    return households_list


def create_workplaces_list(population_size: int, workplaces_infection_rate: float) -> list[Workplace]:
    workplaces_sizes = [i for i in range(1, 51)]
    workplaces_sizes_frequencies = np.loadtxt("data/insee_workplaces.csv", delimiter=",")
    workplaces_list = []

    pop = 0
    id = 0
    while pop < population_size:
        random_workplace_size = generate_random_cluster_size(workplaces_sizes, workplaces_sizes_frequencies)
        while pop + random_workplace_size > population_size:
            random_workplace_size = generate_random_cluster_size(workplaces_sizes, workplaces_sizes_frequencies)
        workplaces_list.append(Workplace(id, random_workplace_size, workplaces_infection_rate))
        id += 1
        pop += random_workplace_size

    return workplaces_list


def generate_random_cluster_size(possible_sizes: list[int], sizes_frequencies: np.ndarray[np.float64]) -> int:
    return int(np.random.choice(possible_sizes, 1, replace=True, p=sizes_frequencies)[0])


if __name__ == "__main__":
    population_size = int(1e3)

    global_infection_rate = 1
    household_infection_rate = 1
    workplace_infection_rate = 1

    healing_rate = 1

    households_list = create_households_list(population_size, household_infection_rate)
    workplaces_list = create_workplaces_list(population_size, workplace_infection_rate)
