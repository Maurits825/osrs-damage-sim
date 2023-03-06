from dataclasses import dataclass
from enum import Enum

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class GraphType(str, Enum):
    TTK_PROBABILITY = "time_to_kill_probability"
    TTK_CUMULATIVE = "time_to_kill_cumulative"


@dataclass()
class Graph:
    figure: Figure
    axes: Axes

    def __init__(self, plt, width, height):
        self.figure = plt.figure(figsize=(width, height))
        self.axes = self.figure.add_subplot()

    def reset(self):
        self.axes.cla()
