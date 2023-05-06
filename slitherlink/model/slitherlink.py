
from slitherlink.solver import SlitherlinkSolver
from .field import Field


class Slitherlink():
    def __init__(self, fieldlist: list[Field]) -> None:
        self.fields = fieldlist
        for field in fieldlist:
            field.slitherlink = self
        self.lines = list(
            set(line for field in self.fields for line in field.linelist))
        self.points = list(
            set(point for field in self.fields for point in field.pointlist))
        self.solver = SlitherlinkSolver(self)

    pass
