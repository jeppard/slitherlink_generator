
from .field import Field


class Slitherlink():
    def __init__(self, fieldlist: list[Field]) -> None:
        self.fieldlist = fieldlist
        self.points = list(
            set([p for field in fieldlist for p in field.pointlist]))
        self.linelist = list(
            set([line for field in fieldlist for line in field.linelist]))

    def hasOnePath(self) -> bool:
        return True  # TODO: Implement
    pass
