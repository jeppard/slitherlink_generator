import tkinter

from slitherlink.gui.gui_options import GUIOptions
from slitherlink.model.line_state import LineState
from ..model.line import Line
from .point import PointGui
import shapely.geometry


class LineGui(Line):
    points: tuple[PointGui, PointGui]

    def __init__(self, points: tuple[PointGui, PointGui]) -> None:
        super().__init__(points)
        self.bbox = shapely.geometry.LineString(
            [p.position for p in points]).buffer(GUIOptions.LINE_BBOX_WIDTH)
        self.bbox -= shapely.geometry.Point(
            points[0].position).buffer(GUIOptions.POINT_RADIUS)
        self.bbox -= shapely.geometry.Point(
            points[1].position).buffer(GUIOptions.POINT_RADIUS)

    def draw(self, canvas: tkinter.Canvas) -> None:
        match (self.state):
            case LineState.UNKNOWN:
                canvas.create_line(self.points[0].x, self.points[0].y,
                                   self.points[1].x, self.points[1].y,
                                   fill=GUIOptions.LINE_ACTIVE_COLOR,
                                   dash=GUIOptions.LINE_DASH,
                                   width=GUIOptions.LINE_WIDTH)
            case LineState.SET:
                canvas.create_line(self.points[0].x, self.points[0].y,
                                   self.points[1].x, self.points[1].y,
                                   fill=GUIOptions.LINE_ACTIVE_COLOR,
                                   width=GUIOptions.LINE_WIDTH)
            case LineState.UNSET:
                canvas.create_line(self.points[0].x, self.points[0].y,
                                   self.points[1].x, self.points[1].y,
                                   fill=GUIOptions.LINE_INACTIVE_COLOR,
                                   dash=GUIOptions.LINE_DASH,
                                   width=GUIOptions.LINE_WIDTH)
            case _:
                raise ValueError("Unknown LineState")

    def onClick(self, clickPos: tuple[int, int]) -> None:
        if self.isClicked(clickPos):
            self.toggleState()

    def isClicked(self, clickPos: tuple[int, int]) -> bool:
        return self.bbox.contains(shapely.geometry.Point(clickPos))