import numpy as np
import copy
import matplotlib.pyplot as plt

from Epidemic import Epidemic
from SocialStructure import Workplaces, Households
from Individual import Individual


def fill_households_and_workplaces(individuals: list[Individual], households: Households, workplaces: Workplaces):
    h = copy.copy(households.clusters)
    w = copy.copy(workplaces.clusters)

    for i in individuals:
        chosen_household = households.get_random_cluster()
        chosen_workplace = workplaces.get_random_cluster()

        i.household = chosen_household
        i.workplace = chosen_workplace

        chosen_household.add_individual(i)
        chosen_workplace.add_individual(i)

        if chosen_household.is_full():
            h.remove(chosen_household)

        if chosen_workplace.is_full():
            w.remove(chosen_workplace)

def generate_time_next_infection_event(infected: int, susceptible: int):
    pass


if __name__ == "__main__":
    np.random.seed(0)

    population_size = int(1e3)

    global_infection_rate = 1
    household_infection_rate = 1
    workplace_infection_rate = 1

    mean_infection_time = 15  # days
    deviation_infection_time = 3

    households = Households(household_infection_rate, population_size)
    workplaces = Workplaces(workplace_infection_rate, population_size)

    individuals = [Individual(id) for id in range(0, population_size)]
    susceptible =  []
    infected = []
    recovered = []

    fill_households_and_workplaces(individuals, households, workplaces)

    max_time = 500  # days

    epidemic = Epidemic(population_size, individuals, global_infection_rate, mean_infection_time, deviation_infection_time, max_time)
    epidemic.global_infection()