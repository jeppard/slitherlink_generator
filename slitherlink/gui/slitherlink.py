from slitherlink.gui.line import LineGui
from slitherlink.model.field import Field
from ..model.slitherlink import Slitherlink
from .field import FieldGui


class SlitherlinkGui(Slitherlink):
    fieldlist: list[FieldGui]
    linelist: list[LineGui]

    def __init__(self, fieldlist: list[FieldGui]) -> None:
        super().__init__(fieldlist)
        self.linelist = list(
            set([line for field in fieldlist for line in field.linelist]))

    def draw(self, screen):
        [field.draw(screen) for field in self.fieldlist]

    def getSize(self) -> tuple[tuple[int, int], tuple[int, int]]:
        minX = min([p.x for field in self.fieldlist for p in field.pointlist])
        maxX = max([p.x for field in self.fieldlist for p in field.pointlist])
        minY = min([p.y for field in self.fieldlist for p in field.pointlist])
        maxY = max([p.y for field in self.fieldlist for p in field.pointlist])
        return (minX, minY), (maxX, maxY)

    def onClick(self, clickPos: tuple[int, int]) -> FieldGui | None:
        for field in self.fieldlist:
            if field.onClick(clickPos):
                return field
        return None

    def isClicked(self, clickPos: tuple[int, int]) -> bool:
        for field in self.fieldlist:
            if field.isClicked(clickPos):
                return True
        return False
