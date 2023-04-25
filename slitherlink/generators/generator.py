
from slitherlink.gui.field import FieldGui
from slitherlink.gui.gui_options import GUIOptions
from ..model.forms import SlitherlinkForm, OuterForm
from ..gui.slitherlink import SlitherlinkGui
from ..gui.point import PointGui
from ..gui.line import LineGui


class SlitherlinkGenerator():
    @staticmethod
    def generate(form: SlitherlinkForm, size: tuple[int, int],
                 outerForm: OuterForm = OuterForm.RECTANGLE) -> None:
        match (form, outerForm):
            case SlitherlinkForm.SQUARE, _:
                slitherlink = SlitherlinkGenerator.generate_square(size)
            case _:
                slitherlink = SlitherlinkGui([])
                # raise ValueError("Unknown form")

        return slitherlink

    @staticmethod
    def generate_square(size: tuple[int, int]) -> SlitherlinkGui:
        points = [
            [PointGui(x * GUIOptions.STEP + GUIOptions.MARGIN,
                      y * GUIOptions.STEP + GUIOptions.MARGIN)
             for x in range(size[0] + 1)]
            for y in range(size[1] + 1)
        ]
        horizontalLines = [
            [LineGui((points[y][x], points[y][x+1])) for x in range(size[0])]
            for y in range(size[1] + 1)
        ]
        verticalLines = [
            [LineGui((points[y][x], points[y+1][x]))
             for x in range(size[0] + 1)]
            for y in range(size[1])
        ]
        fields = [
            FieldGui([
                points[y][x], points[y][x+1],
                points[y+1][x+1], points[y+1][x]
            ],
                [
                horizontalLines[y][x], verticalLines[y][x],
                horizontalLines[y+1][x], verticalLines[y][x+1]
            ])
            for x in range(size[0])
            for y in range(size[1])
        ]
        return SlitherlinkGui(fields)
