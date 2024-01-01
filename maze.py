import sys
from PIL import Image, ImageDraw, ImageFont

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Queue:
    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

    def pop(self):
        if self.contains_in_queue():
            return self.queue.pop(0)
        
    def contains_in_queue(self):
        if len(self.queue) > 0:
            return True
        
class Maze:
    def __init__(self):
        with open(sys.argv[1], "r") as f:
            self.src = f.read()

        self.src = self.src.splitlines()

        self.height = len(self.src)
        self.width = max(len(line) for line in self.src)

        for i, line in enumerate(self.src):
            for j, element in enumerate(line):
                if element == "A":
                    self.start = (i, j)
                elif element == "B":
                    self.end = (i, j)

    def actions(self, row, col):
        action = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1)
        }

        return action
    
    def solve(self):
        queue = Queue()
        self.explored = set()
        path = []
        self.numPath = 0

        start_node = Node(self.start, None, None)
        queue.add(start_node)

        while queue.contains_in_queue():
            current_node = queue.pop()

            if current_node.state == self.end:
                while current_node:
                    path.append(current_node.state)
                    current_node = current_node.parent
                path.reverse()

                return path, self.explored
            
            self.explored.add(current_node.state)
            self.numPath += 1

            for action, (row, col) in self.actions(*current_node.state).items():
                if 0 <= row < self.height and 0 <= col < self.width and "#" not in self.src[row][col] and (row, col) not in self.explored:
                    next_node = Node((row, col), current_node, action)
                    queue.add(next_node)

    def stored(self):
        maze = []

        for i, row in enumerate(self.src):
            rows = ""
            for j, col in enumerate(row):
                if col == "A":
                    rows += "A"
                elif col == "B":
                    rows += "B"
                elif col == "#":
                    rows += "█"
                elif col == " " and (i, j) in self.solve()[0]:
                    rows += "*"
                else:
                    rows += " "
            maze.append(rows)
        
        return maze
    
    def print(self):
        for line in self.stored():
            print(line)

    def output_image(self, maze, show_explored = None, show_result = None):
        cell_size = 50
        cell_border = 2
        
        img = Image.new(
            "RGBA",
            [self.width * cell_size, self.height * cell_size],
            "grey"
        )

        draw = ImageDraw.Draw(img)

        for i, row in enumerate(maze):
            for j, col in enumerate(row):
                x0 = j * cell_size + cell_border - 0.5
                y0 = i * cell_size + cell_border - 0.5
                x1 = (j + 1) * cell_size - cell_border
                y1 = (i + 1) * cell_size - cell_border

                if (i, j) == self.start:
                    #Yellow
                    fill = (250, 238, 2)
                elif (i, j) == self.end:
                    #Blue
                    fill = (66, 99, 245)
                elif col == "█":
                    #Black
                    fill = (5, 5, 5)
                elif (i, j) in self.solve()[0] and show_result:
                    #Green
                    fill = (19, 250, 2)
                elif (i, j) in self.solve()[1] and show_explored:
                    #Red
                    fill = (252, 3, 3)
                else:
                    #White
                    fill = (255, 255, 255)

                draw.rectangle(
                    [x0, y0, x1, y1],
                    fill
                )

        img.save("maze.png")
        img.show()

m = Maze()
m.output_image(m.stored(), True, True)
print("Number of distance had gone:", m.numPath)