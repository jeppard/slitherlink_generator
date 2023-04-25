from enum import Enum


class SlitherlinkForm(Enum):
    SQUARE = 0
    TRIANGLE = 1
    HEXAGON = 2


class OuterForm(Enum):
    RECTANGLE = 0
    SLITHERLINK_FORM = 1
