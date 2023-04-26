import tkinter
from ..model.point import Point
import shapely.geometry
from .gui_options import GUIOptions


class PointGui(Point):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.position = (x, y)

    def updateX(self, x: int) -> None:
        self.x = x
        self.position = (x, self.y)

    def updateY(self, y: int) -> None:
        self.y = y
        self.position = (self.x, y)

    def draw(self, screen: tkinter.Canvas):
        screen.create_oval(self.x - GUIOptions.POINT_RADIUS,
                           self.y - GUIOptions.POINT_RADIUS,
                           self.x + GUIOptions.POINT_RADIUS,
                           self.y + GUIOptions.POINT_RADIUS,
                           fill=GUIOptions.POINT_COLOR,
                           outline=GUIOptions.POINT_COLOR)
