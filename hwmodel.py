import numpy as np
import random
import matplotlib.pyplot as plt
from Cluster import Cluster
from Individual import Individual


def generate_random_int():
    pass


def initialize_clusters_list(cluster_nb: int, cluster_infection_rate: float, population_size: int) -> list[Cluster]:
    [Cluster(id, 0, cluster_infection_rate) for id in range(cluster_nb)]


if __name__ == "__main__":
    population_size = int(1e4)

    households_nb = int(2.5 * 1e3)
    workplaces_nb = int(4 * 1e3)

    global_infection_rate = 1
    household_infection_rate = 1
    workplace_infection_rate = 1

    healing_rate = 1

    # households = initialize_clusters_list(households_nb, household_infection_rate, population_size)
    # workplaces = initialize_clusters_list(workplaces_nb, workplace_infection_rate, population_size)

    # Importer un fichier texte ou CSV dans un array NumPy
    households_sizes = [i for i in range(1, 7)]
    households_sizes_frequencies = np.loadtxt("data/insee_households.csv", delimiter=",")
    workplaces_sizes = [i for i in range(1, 51)]
    workplaces_sizes_frequencies = np.loadtxt("data/insee_workplaces.csv", delimiter=",")

    household_sizes = np.random.choice(households_sizes, households_nb, replace=True,
                                       p=households_sizes_frequencies)

    plt.hist(household_sizes, density=True, align="right")
    plt.show()

    workplace_hist = np.random.choice(workplaces_sizes, workplaces_nb, replace=True, p=workplaces_sizes_frequencies)
    plt.hist(workplace_hist, density=True, align="right")
    plt.show()