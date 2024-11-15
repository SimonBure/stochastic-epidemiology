from shutil import copy2

import numpy as np
import copy
import matplotlib.pyplot as plt
from Cluster import Household, Workplace
from Individual import Individual


def create_households_list(population_size: int, households_infection_rate: float) -> list[Household]:
    households_sizes = [i for i in range(1, 7)]
    households_sizes_frequencies = np.loadtxt("data/insee_households.csv", delimiter=",")
    households = []

    pop = 0
    id = 0
    while pop < population_size:
        random_household_size = generate_random_cluster_size(households_sizes, households_sizes_frequencies)
        while pop + random_household_size > population_size:
            random_household_size = generate_random_cluster_size(households_sizes, households_sizes_frequencies)
        households.append(Household(id, random_household_size, households_infection_rate))
        id += 1
        pop += random_household_size

    return households


def create_workplaces_list(population_size: int, workplaces_infection_rate: float) -> list[Workplace]:
    workplaces_sizes = [i for i in range(1, 51)]
    workplaces_sizes_frequencies = np.loadtxt("data/insee_workplaces.csv", delimiter=",")
    workplaces = []

    pop = 0
    id = 0
    while pop < population_size:
        random_workplace_size = generate_random_cluster_size(workplaces_sizes, workplaces_sizes_frequencies)
        while pop + random_workplace_size > population_size:
            random_workplace_size = generate_random_cluster_size(workplaces_sizes, workplaces_sizes_frequencies)
        workplaces.append(Workplace(id, random_workplace_size, workplaces_infection_rate))
        id += 1
        pop += random_workplace_size

    return workplaces


def generate_random_cluster_size(possible_sizes: list[int], sizes_frequencies: np.ndarray[np.float64]) -> int:
    return np.random.choice(possible_sizes, None, replace=True, p=sizes_frequencies)


def fill_households_and_workplaces(individuals: list[Individual], households: list[Household], workplaces: list[Workplace]):
    h = copy.copy(households)
    w = copy.copy(workplaces)

    for i in individuals:
        chosen_household = np.random.choice(h)
        chosen_workplace = np.random.choice(w)

        i.household = chosen_household
        i.workplace = chosen_workplace

        chosen_household.individuals_inside.append(i)
        chosen_workplace.individuals_inside.append(i)

        if len(chosen_household.individuals_inside) == chosen_household.size:
            h.remove(chosen_household)

        if len(chosen_workplace.individuals_inside) == chosen_workplace.size:
            w.remove(chosen_workplace)


if __name__ == "__main__":
    population_size = int(1e3)

    global_infection_rate = 1
    household_infection_rate = 1
    workplace_infection_rate = 1

    healing_rate = 1

    households = create_households_list(population_size, household_infection_rate)
    workplaces = create_workplaces_list(population_size, workplace_infection_rate)

    individuals = [Individual(id) for id in range(0, population_size)]

    fill_households_and_workplaces(individuals, households, workplaces)

    print(individuals[:3])