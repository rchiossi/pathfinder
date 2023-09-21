from typing import TypeVar, Callable, Iterable, Any, Generic
import logging 


logging.basicConfig(level=logging.DEBUG)

Graph = TypeVar('Graph')
Node = TypeVar('Node')


class AStar(Generic[Graph, Node]):
    def __init__(self, graph: Graph,
                 find_neighbours: Callable[[Graph, Node], list[Node]],
                 edge_cost: Callable[[Graph, Node, Node], int],
                 h: Callable[[Graph, Node, Node], int],
                 max_depth: int = -1) -> None:

        self.graph = graph
        self.find_neighbours = find_neighbours
        self.edge_cost = edge_cost
        self.h = h
        self.max_depth = max_depth

    def find_path(self, start: Node, end: Node) -> list[Node] | None:
        previous : dict[Node, Node] = {}
        cost : dict[Node, int] = {}
        open_set : dict[Node, int] = {}

        open_set[start] = self.h(self.graph, start, end)
        cost[start] = 0
        previous[start] = start

        current_depth = 0
        found = False
        while len(open_set) and not found and (self.max_depth == -1 or current_depth < self.max_depth):
            current_depth += 1

            current = min(open_set, key=lambda k: open_set[k])
            current_cost = cost[current]
            logging.debug(f'current = {current}, cost = {current_cost}')

            open_set.pop(current)

            neighbours = self.find_neighbours(self.graph, current)
            for neighbour in neighbours:
                logging.debug(f'neighbour = {neighbour}')

                if neighbour == start or neighbour == previous[current]:
                    continue

                edge = self.edge_cost(self.graph, current, neighbour)
                neighbour_cost = current_cost + edge

                if  neighbour == end:
                    previous[end] = current
                    found = True
                    break

                if neighbour not in open_set or neighbour_cost < cost[neighbour]:
                    open_set[neighbour] = neighbour_cost + self.h(self.graph, neighbour, end)
                    cost[neighbour] = neighbour_cost
                    previous[neighbour] = current

        if not found:
            return None

        path : list[Node] = [end]
        while previous[path[-1]] != start:
            path.append(previous[path[-1]])

        path.append(start)
        path.reverse()

        return path

