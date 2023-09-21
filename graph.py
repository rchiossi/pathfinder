from astar import AStar

class GeneralNode:
    def __init__(self, name : int, neighbours: dict[int, int]) -> None:
        self.name = name
        self.neighbours = neighbours

    def __str__(self):
        return str(self.name)


class GeneralGraph:
    def __init__(self):
        self.nodes : list[GeneralNode] = []
        self.node_map : dict[int, GeneralNode] = {}

    def __iter__(self):
        return iter(self.nodes)

    def add_node(self, node: GeneralNode) -> None:
        self.nodes.append(node)
        self.node_map[node.name] = node

    def get_node(self, name: int) -> GeneralNode:
        return self.node_map[name]

    def find_neighbours(self, node : GeneralNode) -> list[GeneralNode]:
        neighbours : list[GeneralNode] = []
        for n in node.neighbours:
            neighbours.append(self.node_map[n])
        return neighbours

    def edge_cost(self, start : GeneralNode, end : GeneralNode) -> int:
        return start.neighbours[end.name]

    def h(self, start : GeneralNode, end : GeneralNode) -> int:
        return end.name - start.name


if __name__ == "__main__":
    print("Test General Graph: ")

    g = GeneralGraph()

    g.add_node(GeneralNode(1, {2: 1, 3: 2}))
    g.add_node(GeneralNode(2, {1: 1, 3: 1, 4: 1}))
    g.add_node(GeneralNode(3, {1: 1, 2: 1, 4: 1}))
    g.add_node(GeneralNode(4, {3: 1}))

    pf = AStar(g, GeneralGraph.find_neighbours, GeneralGraph.edge_cost, GeneralGraph.h, 10)
    path = pf.find_path(g.get_node(1), g.get_node(4))

    if path != None:
        for p in path[:-1]:
            print(f'{p.name} -> ', end='')
        print(path[-1].name)
    else:
        print("No Path found!")


