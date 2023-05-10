import dataclasses


@dataclasses.dataclass(order=True, frozen=True)
class Point():
    x: int
    y: int
