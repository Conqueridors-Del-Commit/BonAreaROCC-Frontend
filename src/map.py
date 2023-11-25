from dataclasses import dataclass


@dataclass
class Node:
    """Classe que representa un node d'un graf"""
    x: int
    y: int
    type: str
    representation: str
    neighbours: []


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
