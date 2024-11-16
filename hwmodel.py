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

    global_infection_proba = 1
    household_infection_proba = 1
    workplace_infection_proba = 1

    mean_infection_time = 15  # days
    deviation_infection_time = 3

    workplaces = Workplaces(workplace_infection_proba, population_size)
    households = Households(household_infection_proba, population_size)

    individuals = [Individual(id) for id in range(0, population_size)]
    susceptible =  []
    infected = []
    recovered = []

    fill_households_and_workplaces(individuals, households, workplaces)
    print(workplaces)
    max_time = 5  # days

    epidemic = Epidemic(population_size, individuals, households, workplaces, global_infection_proba,
                        mean_infection_time, deviation_infection_time, max_time)
    epidemic.global_infection()  # first infection

    while epidemic.time < epidemic.max_time or epidemic.susceptible_nb == 0:
        epidemic.generate_next_infection_event()

    susceptible_overtime = epidemic.generate_susceptible_time_series()
    infected_overtime = epidemic.generate_infected_time_series()

    plt.plot(epidemic.times, susceptible_overtime, label='S', color='grey')
    plt.plot(epidemic.times, infected_overtime, label='I', color='red')
    plt.legend(loc='best')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Number of individuals', fontsize=16)

    plt.show()