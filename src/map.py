from dataclasses import dataclass


@dataclass
class Node:
    """Classe que representa un node d'un graf"""
    x: int
    y: int
    type: str
    representation: str
    picking_neighbour_x: int = 0
    picking_neighbour_y: int = 0


@dataclass
class Map:
    """Classe que representa el plànol de la botiga."""
    width: int
    height: int
    grid: []

    def get_node_by_coordinates(self, x, y):
        for node in self.grid:
            if node.x == x and node.y == y:
                return node
        return None

    def set_node_by_coordinates(self, x, y, node):
        to_delete = None
        for nd in self.grid:
            if nd.x == x and nd.y == y:
                to_delete = nd
        if to_delete is not None:
            self.grid.remove(to_delete)
        self.grid.append(node)

