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


def save_results_epidemic(susceptible_timeseries, infected_timeseries, times):
    np.save('epidemics_results', np.array([susceptible_timeseries, infected_timeseries, times]))

def load_results_epidemic():
    return np.load('epidemics_results.npy')


if __name__ == "__main__":
    load = False
    if load:
        susceptible_time_series, infected_time_series, times = load_results_epidemic()

    else:
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

        max_time = 100

        epidemic = Epidemic(population_size, individuals, households, workplaces, global_infection_rate,
                            mean_infection_time, deviation_infection_time, max_time)
        epidemic.first_infection()

        while epidemic.time < epidemic.max_time:
            if epidemic.is_zero_susceptible_remaining():
                epidemic.end_epidemic_()
                break
            else:
                epidemic.generate_next_infection_event()

        susceptible_time_series = epidemic.generate_susceptible_time_series()
        infected_time_series = epidemic.infected_time_series
        times = epidemic.times

        save_results_epidemic(susceptible_time_series, epidemic.infected_time_series, epidemic.times)

        infection_type_freq = epidemic.get_infection_type_frequencies()
        print(f"Frequency of global infection: {infection_type_freq[0]}")
        print(f"Frequency of infections in households: {infection_type_freq[1]}")
        print(f"Frequency of infections in workplaces: {infection_type_freq[2]}")

        frequencies_timeseries = epidemic.get_infection_type_frequencies_timeseries()

        plt.plot(frequencies_timeseries[:, 0], label='Global', color='red')
        plt.plot(frequencies_timeseries[:, 1], label='Household', color='darkred')
        plt.plot(frequencies_timeseries[:, 2], label='Workplace', color='darkorange')
        plt.legend(loc='best')
        plt.xlabel('Number infection', fontsize=16)
        plt.ylabel('Frequency', fontsize=16)
        plt.show()

        print(f"Peak size: {epidemic.get_normalized_peak_size()}")

    plt.plot(times, susceptible_time_series, label='S', color='grey')
    plt.plot(times, infected_time_series, label='I', color='red')
    plt.legend(loc='best')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Number of individuals', fontsize=16)
    plt.show()
