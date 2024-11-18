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


if __name__ == "__main__":
    np.random.seed(0)

    population_size = int(1e3)

    global_infection_rate = 1e-4
    household_infection_rate = 1e-3
    workplace_infection_rate = 5e-4

    mean_infection_time = 15  # days
    deviation_infection_time = 3

    workplaces = Workplaces(workplace_infection_rate, population_size)
    households = Households(household_infection_rate, population_size)

    individuals = [Individual(id) for id in range(0, population_size)]
    susceptible =  []
    infected = []
    recovered = []

    fill_households_and_workplaces(individuals, households, workplaces)
    # print(workplaces.clusters[0].susceptible)
    max_time = 500  # days

    epidemic = Epidemic(population_size, individuals, households, workplaces, global_infection_rate,
                        mean_infection_time, deviation_infection_time, max_time)
    epidemic.global_infection()  # first infection

    while epidemic.time < epidemic.max_time or epidemic.susceptible_nb == 0:
        if epidemic.is_zero_susceptible_remaining():
            epidemic.end_epidemic_()
            break
        else:
            epidemic.generate_next_infection_event()

    susceptible_time_series = epidemic.generate_susceptible_time_series()
    print(epidemic.times)
    plt.plot(epidemic.times, susceptible_time_series, label='S', color='grey')
    plt.plot(epidemic.times, epidemic.infected_time_series, label='I', color='red')
    plt.legend(loc='best')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Number of individuals', fontsize=16)

    plt.show()