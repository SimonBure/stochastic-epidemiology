import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    max_time = 100
    time_step = 0.1

    population_size = 1e3

    healing_rate = 0.001
    infection_rate = 0.004

    susceptible = population_size - 1
    infected = 1
    recovered = 0

    array_size = int(max_time // time_step)

    time_array = np.linspace(0, max_time, array_size)

    susceptible_arr = susceptible * np.ones(array_size)
    infected_arr = infected * np.ones(array_size)
    recovered_arr = recovered * np.ones(array_size)

    for index in range(1, array_size):
        susceptible += time_step * (-infection_rate * susceptible * infected)
        infected += time_step * (infection_rate * susceptible * infected - healing_rate * infected)
        recovered += time_step * (healing_rate * infected)

        susceptible_arr[index] = susceptible
        infected_arr[index] = infected
        recovered_arr[index] = recovered

    plt.plot(time_array, susceptible_arr, label='susceptible', color='grey')
    plt.plot(time_array, infected_arr, label='infected', color='red')
    plt.plot(time_array, recovered_arr, label='recovered', color='green')
    plt.legend()
    plt.show()
