import polylabel
import shapely.geometry
import tkinter

from slitherlink.util.dashed_image_draw import DashedImageDraw
from .point import PointGui
from .line import LineGui
from ..model.field import Field
from ..model.point import Point
from ..model.line import Line
from .gui_options import GUIOptions
from PIL import ImageFont


class FieldGui(Field):
    pointlist: list[PointGui]
    linelist: list[LineGui]

    def __init__(self, pointlist: list[PointGui],
                 linelist: list[Line]) -> None:
        super().__init__(pointlist, linelist)
        self.bbox = shapely.geometry.Polygon(
            [(point.x, point.y) for point in pointlist])
        self.middle = polylabel.polylabel([
            [(point.x, point.y) for point in pointlist]])
        self.selected = False

    def draw(self, screen: tkinter.Canvas, selected: bool = False):
        [line.draw(screen) for line in self.linelist]
        [point.draw(screen) for point in self.pointlist]
        if selected:
            screen.create_polygon(
                [point.position for point in self.pointlist],
                fill=GUIOptions.FIELD_SELECTED_COLOR)
        if self.number is not None:
            screen.create_text(int(self.middle[0]), int(self.middle[1]),
                               text=str(self.number), font=GUIOptions.FONT,
                               anchor="center")

    def drawImage(self, drawable: DashedImageDraw):
        [line.drawImage(drawable) for line in self.linelist]
        [point.drawImage(drawable) for point in self.pointlist]
        if self.number is not None:
            drawable.text((int(self.middle[0]), int(
                self.middle[1])), str(self.number), anchor="mm",
                font=ImageFont.truetype(GUIOptions.FONT_TTF,
                                        GUIOptions.FONT_TTF_SIZE),
                fill=GUIOptions.FONT_COLOR)

    def onClick(self, clickPos: tuple[int, int]) -> bool:
        for line in self.linelist:
            line.onClick(clickPos)
        return self.isClicked(clickPos)

    def isClicked(self, clickPos: tuple[int, int]) -> bool:
        for line in self.linelist:
            if line.isClicked(clickPos):
                return False
        return self.bbox.contains(shapely.geometry.Point(clickPos))
