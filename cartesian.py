from astar import AStar
import math

class CartesianGraph:
    def __init__(self):
        self.map : list[list[str]] = []

        self.x = -1
        self.y = -1

    def __str__(self):
        return f'CartesianMap[{self.x}, {self.y}]'

    def load_from_file(self, filename: str):
        with open(filename, 'r') as f:
            data = f.read()

        lines = data.split('\n')
        self.x = int(lines[0])
        self.y = int(lines[1])

        for n in range(self.y):
            self.map.append([l for l in lines[2 + n]])

    def print_map(self):
        for l in self.map:
            #print(' '.join(l))
            for item in l:
                if len(item) == 1:
                    print(f' {item} ', end='')
                else:
                    print(f'{item} ', end='')
            print()

    def find_neighbours(self, node: tuple[int, int]) -> list[tuple[int, int]]:
        neighbours : list[tuple[int,int]] = []

        x = node[0]
        y = node[1]

        #top left
        #if x > 0 and y > 0 and self.map[y-1][x-1] != '#':
        #    neighbours.append((x-1, y-1))

        #top middle
        if y > 0 and self.map[y-1][x] != '#':
            neighbours.append((x, y - 1))

        #top right
        #if x < self.x - 2 and y > 0 and self.map[y-1][x+1] != '#':
        #    neighbours.append((x + 1, y - 1))

        #left
        if x > 0 and self.map[y][x - 1] != '#':
            neighbours.append((x - 1, y))

        #right
        if x < self.x - 2 and self.map[y][x+1] != '#':
            neighbours.append((x + 1, y))

        #bottom left
        #if x > 0 and y < self.y - 2 and self.map[y+1][x-1] != '#':
        #    neighbours.append((x - 1, y + 1))

        #bottom middle
        if y < self.y - 2 and self.map[y+1][x] != '#':
            neighbours.append((x, y + 1))

        #bottom right
        #if x < self.x - 2 and y < self.y - 2 and self.map[y+1][x+1] != '#':
        #    neighbours.append((x + 1, y + 1))

        return neighbours


    def edge_cost(self, _start: tuple[int, int], _end: tuple[int, int]) -> int: #pyright: ignore
        return 1

    def h(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        #return int(math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) * 10)
        return (abs(start[0] - end[0]) + abs(start[1] - end[1]))


if __name__ == '__main__':
    g = CartesianGraph()

    g.load_from_file("example.map")
    g.print_map()

    pf = AStar(g, CartesianGraph.find_neighbours, CartesianGraph.edge_cost, CartesianGraph.h, 100)
    path = pf.find_path((1, 1), (8, 8))

    g.print_map()

    if path != None:
        for p in path[:-1]:
            print(f'{p} -> ', end='')
            g.map[p[1]][p[0]] = '*'
        print(path[-1])
        g.map[path[-1][1]][path[-1][0]] = '*'
    else:
        print("No Path found!")

    g.print_map()




