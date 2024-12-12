from enum import Enum

class Direction(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    def x(self):
        return self.value[0]
    
    def y(self):
        return self.value[1]
    
    def perpendicular(self):
        if self == Direction.UP or self == Direction.DOWN:
            return Direction.RIGHT, Direction.LEFT
        return Direction.UP, Direction.DOWN

class Plot:
    def __init__(self, x, y, plant):
        self.plant = plant
        self.x = x
        self.y = y
        self.region = None
        self.borders = []

class Region:
    def __init__(self, plots, garden):
        self.plots = plots
        self.garden = garden

    def get_area(self):
        return len(self.plots)
    
    def get_perimeter(self):
        return sum([len(plot.borders) for plot in self.plots])
    
    def get_sides(self):
        sides = 0
        borders = [(plot, border) for plot in self.plots for border in plot.borders]
        while len(borders):
            sides += 1
            plot, border = borders.pop()
            for direction in border.perpendicular():
                other_plot = self.garden.get_in_dir(plot, direction)
                while other_plot is not None and other_plot.region == self and border in other_plot.borders:
                    borders.remove((other_plot, border))
                    other_plot = self.garden.get_in_dir(other_plot, direction)

        return sides


class Garden:
    def __init__(self, file):
        self.plots = []
        with open(file) as f:
            for y, line in enumerate(f):
                self.plots.append([])
                for x, plant in enumerate(line.strip()):
                    self.plots[y].append(Plot(x, y, plant))

        self.width = len(self.plots[0])
        self.height = len(self.plots)

        self.generate_regions()

    def is_in_garden(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_plot(self, x, y):
        if self.is_in_garden(x, y):
            return self.plots[y][x]
        return None

    def get_contigous_plots(self, plot, contigous_plots = None):
        if contigous_plots is None:
            contigous_plots = [plot]

        plot.borders = []
        for other_plot, direction in self.get_adjacent_plots(plot):
            if other_plot is not None and other_plot.plant == plot.plant:
                if other_plot not in contigous_plots:
                    contigous_plots.append(other_plot)
                    self.get_contigous_plots(other_plot, contigous_plots)
            else:
                plot.borders.append(direction)

        return contigous_plots
    
    def get_in_dir(self, plot, direction):
        x, y = plot.x + direction.x(), plot.y + direction.y()
        return self.get_plot(x, y)
    
    def get_adjacent_plots(self, plot):
        adjacent_plots = []
        for direction in Direction:
            other_plot = self.get_in_dir(plot, direction)
            adjacent_plots.append((other_plot, direction))
        return adjacent_plots

    def generate_regions(self):
        self.regions = []
        for row in self.plots:
            for plot in row:
                if plot.region is None:
                    contigous_plots = self.get_contigous_plots(plot)
                    region = Region(contigous_plots, self)
                    for contigous_plot in contigous_plots:
                        contigous_plot.region = region
                    self.regions.append(region)

    def get_price(self, discount = False):
        if discount:
            return sum([region.get_area() * region.get_sides() for region in self.regions])

        return sum([region.get_area() * region.get_perimeter() for region in self.regions])

garden = Garden("12/input")
print(garden.get_price())
print(garden.get_price(True))