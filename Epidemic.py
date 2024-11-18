import numpy as np

from Cluster import Cluster
from Individual import Individual
from SocialStructure import Households, Workplaces


class Epidemic:
    population_size: int
    susceptible: list[Individual]
    susceptible_nb: int
    infected: list[Individual]
    infected_nb: int
    infected_time_series: list[int]
    recovered_nb: int

    global_infection_rate: float

    households: Households
    workplaces: Workplaces

    mean_infection_time: float
    deviation_infection_rate: float

    time: float
    times: list[float]
    max_time: float

    def __init__(self, population_size: int, individuals: list[Individual], households: Households,
                 workplaces: Workplaces, global_infection_rate: float, mean_infection_time: float,
                 deviation_infection_rate: float, max_time: float):
        self.population_size = population_size
        self.susceptible = individuals
        self.susceptible_nb = self.population_size
        self.infected = []
        self.infected_nb = 0
        self.infected_time_series = [0]
        self.recovered_nb = 0

        self.households = households
        self.workplaces = workplaces

        self.global_infection_rate = global_infection_rate

        self.mean_infection_time = mean_infection_time
        self.deviation_infection_rate = deviation_infection_rate

        self.time = 0
        self.times = [0]
        self.max_time = max_time

    def __repr__(self):
        return f"Epidemic time: {self.time}. {self.infected_nb} infected. Recovered {self.recovered_nb}."

    def generate_next_infection_event(self):
        global_infection_rate = self.get_global_infection_rate()
        infected_households = self.households.get_infected_clusters()
        infected_workplaces = self.workplaces.get_infected_clusters()
        households_infection_rates = self.households.get_infection_rates(infected_households)
        workplaces_infection_rates = self.workplaces.get_infection_rates(infected_workplaces)  #

        total_rate = global_infection_rate + sum(households_infection_rates) + sum(workplaces_infection_rates)

        time_infection = self.generate_time_next_infection_event(total_rate)
        self.time += time_infection
        self.times.append(self.time)
        self.update_infection_times(time_infection)

        global_infection_proba = global_infection_rate / total_rate
        household_infection_proba = sum(households_infection_rates) / total_rate
        workplace_infection_proba = sum(workplaces_infection_rates) / total_rate
        infection_probabilities = [global_infection_proba, household_infection_proba, workplace_infection_proba]

        infection_events = ["global", "household", "workplace"]
        chosen_event = np.random.choice(infection_events, p=infection_probabilities)
        if chosen_event == "global":
            self.global_infection()
        elif chosen_event == "household":
            self.infection_in_cluster(infected_households, (households_infection_rates / sum(households_infection_rates)))
        else:
            self.infection_in_cluster(infected_workplaces, (workplaces_infection_rates / sum(workplaces_infection_rates)))

        self.fill_infected_time_series()

    def get_global_infection_rate(self) -> float:
        return self.global_infection_rate * self.susceptible_nb * self.infected_nb

    @staticmethod
    def generate_time_next_infection_event(rate: float) -> float:
        return np.random.exponential(scale=(1 / rate))

    def update_infection_times(self, time_passed: float):
        for i in self.infected:
            i.update_remaining_infection_duration(time_passed)
            if i.is_cured():
                self.infected.remove(i)
                self.infected_nb -= 1
                self.recovered_nb += 1

    def global_infection(self):
        chosen_susceptible = np.random.choice(self.susceptible)
        self.susceptible.remove(chosen_susceptible)

        chosen_susceptible.infection(self.generate_random_infection_time())
        self.infected.append(chosen_susceptible)

        self.susceptible_nb -= 1
        self.infected_nb += 1

    def generate_random_infection_time(self) -> float:
        return np.random.normal(self.mean_infection_time, self.deviation_infection_rate)

    def infection_in_cluster(self, infected_clusters: list[Cluster], clusters_infection_proba: list[float]):
        chosen_cluster = np.random.choice(infected_clusters, p=clusters_infection_proba)
        rdm_infection_duration = self.generate_random_infection_time()

        chosen_susceptible = chosen_cluster.get_random_susceptible()
        chosen_susceptible.infection(rdm_infection_duration)
        self.infected.append(chosen_susceptible)
        self.susceptible.remove(chosen_susceptible)

        self.susceptible_nb -= 1
        self.infected_nb += 1

    def is_zero_susceptible_remaining(self) -> bool:
        return self.susceptible_nb == 0

    def end_epidemic_(self):
        infection_durations = self.get_all_sorted_remaining_infection_durations()
        for t in infection_durations:
            self.times.append(t)
            self.infected_nb -= 1
            self.fill_infected_time_series()
        self.time = infection_durations[-1]

    def fill_susceptible_time_series(self):
        self.susceptible_time_series.append(self.susceptible_nb)

    def fill_infected_time_series(self):
        self.infected_time_series.append(self.infected_nb)

    def get_all_sorted_remaining_infection_durations(self) -> list[float]:
        remaining_infection_durations = []
        print(len(self.infected))
        for i in self.infected:
            remaining_infection_durations.append(i.remaining_infection_duration)
        remaining_infection_durations.sort()
        return remaining_infection_durations

    def generate_susceptible_time_series(self) -> list[int]:
        if len(self.times) > self.population_size:
            susceptible_time_series = [self.population_size - i for i in range(self.population_size)]
            susceptible_time_series += [0] * (len(self.times) - len(susceptible_time_series))
        else:
            susceptible_time_series = [self.population_size - i for i in range(len(self.times))]
        return susceptible_time_series
