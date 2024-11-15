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

        chosen_household.add_individual(i)
        chosen_workplace.add_individual(i)

        if chosen_household.is_full():
            h.remove(chosen_household)

        if chosen_workplace.is_full():
            w.remove(chosen_workplace)


def generate_random_infection_time(mean: float, deviation: float) -> float:
    return np.random.normal(mean, deviation)

if __name__ == "__main__":
    np.random.seed(0)

    population_size = int(1e3)

    global_infection_rate = 1
    household_infection_rate = 1
    workplace_infection_rate = 1

    mean_infection_time = 15  # days
    deviation_infection_time = 3

    households = create_households_list(population_size, household_infection_rate)
    workplaces = create_workplaces_list(population_size, workplace_infection_rate)

    individuals = [Individual(id) for id in range(0, population_size)]

    fill_households_and_workplaces(individuals, households, workplaces)

    first_infected = np.random.choice(individuals)
    first_infected.infection(generate_random_infection_time(mean_infection_time, deviation_infection_time))
    first_infected.household.infection_event()
    first_infected.workplace.infection_event()
    print(first_infected)
    print(households[79])
    print(workplaces[13])

    time = 0
    max_time = 500
