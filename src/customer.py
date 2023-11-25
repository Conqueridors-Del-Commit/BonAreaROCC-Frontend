import dataclasses


@dataclasses.dataclass
class Customer:
    movements: []
    picking: []
    timestamps: []

    current_x: int = 0
    current_y: int = 0

    destination_x: int = 0
    destination_y: int = 0

    active = False
    completed = False

    picking_rn = False
    current_pick_x: int = 0
    current_pick_y: int = 0
