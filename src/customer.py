import dataclasses


@dataclasses.dataclass
class Customer:
    customer_id: str
    ticket_id: str
    movements: []
    picking: []
    timestamps: []
    color: []

    picked_articles: int = 0
    total_articles: int = 0

    current_x: int = 0
    current_y: int = 0

    destination_x: int = 0
    destination_y: int = 0

    active = False
    completed = False

    picking_rn = False
    current_pick_x: int = 0
    current_pick_y: int = 0
