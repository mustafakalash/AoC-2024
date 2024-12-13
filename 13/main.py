class Button:
    A_COST = 3
    B_COST = 1

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

class Machine:
    FIX_OFFSET = 10000000000000

    def __init__(self, a_button, b_button, prize_x, prize_y):
        self.a_button = a_button
        self.b_button = b_button
        self.prize_x = prize_x
        self.prize_y = prize_y

    def calculate_cost(self, error_fixed):
        prize_x = self.prize_x
        prize_y = self.prize_y
        if error_fixed:
            prize_x += Machine.FIX_OFFSET
            prize_y += Machine.FIX_OFFSET

        b_presses = (self.a_button.dy * prize_x) - (self.a_button.dx * prize_y)
        denominator = (self.a_button.dy * self.b_button.dx) - (self.a_button.dx * self.b_button.dy)
        if denominator == 0:
            return 0
        b_presses /= denominator

        a_presses = (prize_x - (self.b_button.dx * b_presses)) / self.a_button.dx

        if not a_presses.is_integer() or not b_presses.is_integer():
            return 0

        return a_presses * Button.A_COST + b_presses * Button.B_COST
    
class Arcade:
    def __init__(self, file):
        self.machines = []
        with open(file) as f:
            lines = iter(f)
            while True:
                try:
                    get_coords = lambda line, sep: map(lambda coord: int(coord.split(sep)[1]), line.split(","))
                    a_dx, a_dy = get_coords(next(lines), "+")
                    a_button = Button(a_dx, a_dy)
                    b_dx, b_dy = get_coords(next(lines), "+")
                    b_button = Button(b_dx, b_dy)
                    self.prize_x, self.prize_y = get_coords(next(lines), "=")
                    self.machines.append(Machine(a_button, b_button, self.prize_x, self.prize_y))
                    next(lines)
                except StopIteration:
                    break

    def calculate_costs(self, error_fixed = False):
        return sum([machine.calculate_cost(error_fixed) for machine in self.machines])
    
arcade = Arcade("13/input")
print(arcade.calculate_costs())
print(arcade.calculate_costs(True))