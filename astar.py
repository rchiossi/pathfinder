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
        estimate : dict[Node, int] = {}
        open_set : dict[Node, int] = {}

        open_set[start] = self.h(self.graph, start, end)
        cost[start] = 1
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

                estimate_cost = neighbour_cost + self.h(self.graph, neighbour, end)

                if neighbour not in estimate or estimate_cost < estimate[neighbour]:
                    open_set[neighbour] = estimate_cost
                    estimate[neighbour] = estimate_cost
                    cost[neighbour] = neighbour_cost
                    previous[neighbour] = current
                    #self.graph.map[neighbour[1]][neighbour[0]] = f'{estimate_cost}'

            #self.graph.print_map()

        logging.debug(f'found={found} - depth={current_depth}')

        if not found:
            logging.info(f'Path not found - depth = {current_depth}')
            return None

        path : list[Node] = [end]
        current_depth = 0
        while previous[path[-1]] != start and current_depth < self.max_depth:
            current_depth+=1
            path.append(previous[path[-1]])

        if current_depth == self.max_depth:
            logging.error("Loop detected while reconstructing the path.")
            return None

        path.append(start)
        path.reverse()

        return path

