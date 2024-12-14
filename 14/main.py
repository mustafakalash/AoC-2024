class Robot:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

class Grid:
    def __init__(self, file, width, height):
        self.robots = []
        self.width = width
        self.height = height

        with open(file) as f:
            for line in f:
                coords = line.split(" ")
                x, y = map(int, coords[0].split("=")[1].split(","))
                vel_x, vel_y = map(int, coords[1].split("=")[1].split(","))
                self.robots.append(Robot(x, y, vel_x, vel_y))
    
    def calculate_safety(self):
        mid_x = self.width // 2
        mid_y = self.height // 2
        quads = [0, 0, 0, 0]
        for robot in self.robots:
            if robot.x == mid_x or robot.y == mid_y:
                continue

            if robot.x < mid_x and robot.y < mid_y:
                quads[0] += 1
            elif robot.x > mid_x and robot.y < mid_y:
                quads[1] += 1
            elif robot.x < mid_x and robot.y > mid_y:
                quads[2] += 1
            else:
                quads[3] += 1

        return quads[0] * quads[1] * quads[2] * quads[3]
    
    def simulate(self, seconds):
        for robot in self.robots:
            robot.x += robot.vel_x * seconds 
            robot.x %= self.width
            if robot.x < 0:
                robot.x += self.width
            robot.y += robot.vel_y * seconds 
            robot.y %= self.height
            if robot.y < 0:
                robot.y += self.height

    def tree_seconds(self):
        seconds = 0
        while True:
            self.simulate(1)
            seconds += 1
            positions = []
            duplicate = False
            for robot in self.robots:
                if (robot.x, robot.y) in positions:
                    duplicate = True
                    break
                else:
                    positions.append((robot.x, robot.y))

            if not duplicate:
                grid.simulate(-seconds)
                return seconds
        
    def get_grid(self, quads = False):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        for robot in self.robots:
            tile = grid[robot.y][robot.x]
            if tile == ".":
                tile = "1"
            else:
                tile = str(int(tile) + 1)

            grid[robot.y][robot.x] = tile

        if quads:
            mid_x = self.width // 2
            mid_y = self.height // 2
            for y in range(self.height):
                for x in range(self.width):
                    if y == mid_y or x == mid_x:
                        grid[y][x] = " "

        return "\n".join(["".join(row) for row in grid])
    
    def __str__(self):
        return self.get_grid() 
    
grid = Grid("14/input", 101, 103)
grid.simulate(100)
safety = grid.calculate_safety()
grid.simulate(-100)
seconds = grid.tree_seconds()
grid.simulate(seconds)
print(grid)
print("Part 1:", safety, "Part 2:", seconds)