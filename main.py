import arcade
import random
import opensimplex

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#Grid size
GRID_SIZE = 20


class A_star:
    def __init__(self, start, end, grid):
        self.start = start
        self.end = end
        self.grid = grid
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.current = None
        self.start_node = None
        self.end_node = None
        self.setup()
        self.run()

    def setup(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j] = node(i, j, self.grid[i][j])
        self.start_node = self.grid[self.start[0]][self.start[1]]
        self.end_node = self.grid[self.end[0]][self.end[1]]
        self.open_list.append(self.start_node)

    def run(self):
        while len(self.open_list) > 0:
            self.current = self.open_list[0]
            for node in self.open_list:
                if node.f < self.current.f:
                    self.current = node
            self.open_list.remove(self.current)
            self.closed_list.append(self.current)

            if self.current == self.end_node:
                self.path = []
                while self.current != self.start_node:
                    self.path.append(self.current)
                    self.current = self.current.parent
                self.path.append(self.start_node)
                self.path.reverse()
                return self.path

            for node in self.get_neighbours(self.current):
                if node in self.closed_list:
                    continue
                if node not in self.open_list:
                    self.open_list.append(node)
                node.parent = self.current
                node.g = self.current.g + 1
                node.h = abs(node.x - self.end_node.x) + abs(node.y - self.end_node.y)
                node.f = node.g + node.h

    def get_neighbours(self, node):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = node.x + i
                y = node.y + j
                if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]):
                    continue
                if self.grid[x][y].value == 0:
                    continue
                neighbours.append(self.grid[x][y])
        return neighbours


class node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


class Show(arcade.Window):

    def __init__(self):
        #create the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "A* Pathfinding")
        #create the grid with grid_size
        self.grid = [[1 for i in range(SCREEN_HEIGHT // GRID_SIZE)] for j in range(SCREEN_WIDTH // GRID_SIZE)]
        #create the start and end points
        self.start = (0, 0)
        self.end = (SCREEN_WIDTH // GRID_SIZE - 1, SCREEN_HEIGHT // GRID_SIZE - 1)
        # create list of walls with noise
        self.walls = []
        self.obstacle_rect((5, 5), (10, 10))
        #create the path
        self.path = A_star(self.start, self.end, self.grid).path
        #set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def obstacle_rect(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.obstacle(x, y)

    def obstacle_line(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.obstacle(x1, y)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.obstacle(x, y1)

    def obstacle(self, x, y):
        self.walls.append((x, y))
        self.grid[x][y] = 0

    def render_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if (i, j) in self.walls:
                    arcade.draw_rectangle_filled(i * GRID_SIZE + GRID_SIZE // 2, j * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, GRID_SIZE, (100, 100, 100))
                elif (i, j) == self.start:
                    arcade.draw_rectangle_filled(i * GRID_SIZE + GRID_SIZE // 2, j * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, GRID_SIZE, arcade.color.GREEN)
                elif (i, j) == self.end:
                    arcade.draw_rectangle_filled(i * GRID_SIZE + GRID_SIZE // 2, j * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, GRID_SIZE, arcade.color.RED)
                else:
                    arcade.draw_rectangle_filled(i * GRID_SIZE + GRID_SIZE // 2, j * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, GRID_SIZE, (51, 51, 51))
        for node in self.path:
            if node != self.start and node != self.end:
                arcade.draw_rectangle_filled(node.x * GRID_SIZE + GRID_SIZE // 2, node.y * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, GRID_SIZE, (30, 144, 10))



if __name__ == "__main__":
    window = Show()
    arcade.start_render()
    window.render_grid()
    arcade.finish_render()
    arcade.run()
