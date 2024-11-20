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
        return f"Epidemic time: {self.time}. {self.infected_nb} infected. {self.recovered_nb} recovered."

    def first_infection(self):
        first_infected = np.random.choice(self.susceptible)
        self.infection(first_infected)

    def infection(self, infected: Individual):
        infection_duration = self.generate_random_infection_time()
        infected.infection(infection_duration)

        infected.workplace.remove_susceptible(infected)
        infected.workplace.update_after_infection()
        infected.household.remove_susceptible(infected)
        infected.household.update_after_infection()

        self.susceptible.remove(infected)
        self.susceptible_nb -= 1
        self.infected.append(infected)
        self.infected_nb += 1

        if infected.household not in self.households.infected_clusters:
            self.households.add_infected_cluster(infected.household)
        if infected.workplace not in self.workplaces.infected_clusters:
            self.workplaces.add_infected_cluster(infected.workplace)

        if infected.household.is_zero_susceptible_inside():
            self.households.remove_infected_cluster(infected.household)
        if infected.workplace.is_zero_susceptible_inside():
            self.workplaces.remove_infected_cluster(infected.workplace)


    def generate_next_infection_event(self):
        global_infection_rate = self.get_global_infection_rate()
        households_infection_rates = self.households.get_clusters_infection_rates()
        sum_households_infection_rate = np.sum(households_infection_rates)

        workplaces_infection_rates = self.workplaces.get_clusters_infection_rates()
        sum_workplaces_infection_rate = np.sum(workplaces_infection_rates)

        total_rate = global_infection_rate + sum_households_infection_rate + sum_workplaces_infection_rate

        time_infection = self.generate_time_next_infection_event(total_rate)
        self.time += time_infection
        self.times.append(self.time)

        self.update_infection_times(time_infection)

        proba_infection_in_global = global_infection_rate / total_rate

        proba_infection_in_household = sum_households_infection_rate / total_rate
        all_households_infection_proba = households_infection_rates / sum_households_infection_rate

        proba_infection_in_workplace = sum_workplaces_infection_rate / total_rate
        all_workplaces_infection_proba = workplaces_infection_rates / sum_workplaces_infection_rate

        infection_probabilities = (proba_infection_in_global, proba_infection_in_household, proba_infection_in_workplace)

        chosen_susceptible = self.chose_susceptible_for_infection(infection_probabilities,
                                                                  all_households_infection_proba,
                                                                  all_workplaces_infection_proba)
        self.infection(chosen_susceptible)

        self.fill_infected_time_series()

    def chose_susceptible_for_infection(self, infection_probabilities: tuple[float, float, float],
                                        households_infection_rates, workplaces_infection_rates) -> Individual:
        infection_types = ["global", "household", "workplace"]
        chosen_event = np.random.choice(infection_types, p=infection_probabilities)
        if chosen_event == "global":
            chosen_susceptible = np.random.choice(self.susceptible)
        elif chosen_event == "household":
            random_household = self.households.get_random_infected_cluster(households_infection_rates)
            chosen_susceptible = random_household.get_random_susceptible()
        else:
            random_workplace = self.workplaces.get_random_infected_cluster(workplaces_infection_rates)
            chosen_susceptible = random_workplace.get_random_susceptible()

        return chosen_susceptible

    def get_global_infection_rate(self) -> float:
        return self.global_infection_rate * self.susceptible_nb * self.infected_nb

    def get_households_infection_rate(self) -> float:
        return self.households.infection_rate * self.susceptible_nb * self.infected_nb

    def get_workplaces_infection_rate(self) -> float:
        return self.workplaces.infection_rate * self.susceptible_nb * self.infected_nb


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
        last_t = 0
        for t in infection_durations:
            self.time += t - last_t
            self.times.append(self.time)
            self.infected_nb -= 1
            self.fill_infected_time_series()
            last_t = t

    def fill_infected_time_series(self):
        self.infected_time_series.append(self.infected_nb)

    def get_all_sorted_remaining_infection_durations(self) -> list[float]:
        remaining_infection_durations = []
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
