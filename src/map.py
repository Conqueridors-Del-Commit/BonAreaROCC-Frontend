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
        return self.grid[x, y]

    def set_node_by_coordinates(self, x, y, node):
        self.grid[x, y] = node

