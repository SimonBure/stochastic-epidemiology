import abc

class Cluster(abc.ABC):
    id: int
    size: int
    susceptible_nb: int
    infection_rate: float

    def __init__(self, id: int, size: int, susceptible_nb: int, infection_rate: float):
        self.id = id
        self.size = size
        self.susceptible_nb = susceptible_nb
        self.infection_rate = infection_rate
