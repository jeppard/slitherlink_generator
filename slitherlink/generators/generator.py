
from slitherlink.gui.field import FieldGui
from slitherlink.gui.gui_options import GUIOptions
from ..model.forms import SlitherlinkForm, OuterForm
from ..gui.slitherlink import SlitherlinkGui
from ..gui.point import PointGui
from ..gui.line import LineGui


class SlitherlinkGenerator():
    @staticmethod
    def generate(form: SlitherlinkForm, size: tuple[int, int],
                 outerForm: OuterForm = OuterForm.RECTANGLE) -> SlitherlinkGui:
        match (form, outerForm):
            case SlitherlinkForm.SQUARE, _:
                slitherlink = SlitherlinkGenerator.generate_square(size)
            case SlitherlinkForm.HEXAGON, OuterForm.RECTANGLE:
                slitherlink = SlitherlinkGenerator.generate_hexagon_rectange(
                    size)
            case SlitherlinkForm.HEXAGON, OuterForm.SLITHERLINK_FORM:
                slitherlink = SlitherlinkGenerator.generate_hexagon_hexagon(
                    size[0])
            case SlitherlinkForm.TRIANGLE, OuterForm.RECTANGLE:
                slitherlink = SlitherlinkGenerator.generate_triangle_rectange(
                    size)
            case _:
                slitherlink = SlitherlinkGui([])
                raise ValueError("Unknown form")

        return slitherlink

    @staticmethod
    def generate_triangle_rectange(size: tuple[int, int]) -> SlitherlinkGui:
        points = tuple(
            tuple(
                PointGui((2 * x + y % 2) * GUIOptions.STEP + GUIOptions.MARGIN,
                         y * (3*GUIOptions.STEP)//2 + GUIOptions.MARGIN)
                for x in range(size[0] + 1)
            )
            for y in range(size[1] + 1)
        )
        horizontalLines = tuple(
            tuple(
                LineGui((points[y][x], points[y][x+1])) for x in range(size[0])
            ) for y in range(size[1] + 1)
        )
        verticalLines = tuple(
            tuple(
                LineGui((
                    points[y + (y % 2)][(x+1)//2],
                    points[y+1-(y % 2)][x//2],
                ))
                for x in range(2*size[0]+1)
            )
            for y in range(size[1])
        )
        fields = [
            FieldGui([
                points[y][x//2 + (x % 2) * (y % 2 == 0)],
                points[y + (x+y) % 2][x//2 + 1],
                points[y+1][(x + y % 2)//2],
            ],
                [horizontalLines[y+x % 2][x//2],
                 verticalLines[y][x+1-x % 2],
                 verticalLines[y][x+(x % 2)]])
            for y in range(size[1])
            for x in range(2*size[0])
        ]
        return SlitherlinkGui(fields)

    @staticmethod
    def generate_square(size: tuple[int, int]) -> SlitherlinkGui:
        points = tuple(
            tuple(PointGui(x * GUIOptions.STEP + GUIOptions.MARGIN,
                           y * GUIOptions.STEP + GUIOptions.MARGIN)
                  for x in range(size[0] + 1))
            for y in range(size[1] + 1)
        )
        horizontalLines = tuple(
            tuple(LineGui((points[y][x], points[y][x+1]))
                  for x in range(size[0]))
            for y in range(size[1] + 1)
        )
        verticalLines = tuple(
            tuple(LineGui((points[y][x], points[y+1][x]))
                  for x in range(size[0] + 1))
            for y in range(size[1])
        )
        fields = [
            FieldGui([
                points[y][x], points[y][x+1],
                points[y+1][x+1], points[y+1][x]
            ],
                [
                horizontalLines[y][x], verticalLines[y][x],
                horizontalLines[y+1][x], verticalLines[y][x+1]
            ])
            for y in range(size[1])
            for x in range(size[0])
        ]
        return SlitherlinkGui(fields)

    @staticmethod
    def getHexagonPosition(x: int, y: int, offset=False) -> tuple[int, int]:
        return ((2*x + (y % 4 in [0, 3])) * GUIOptions.STEP +
                GUIOptions.MARGIN - (offset * GUIOptions.STEP),
                ((y + y//2) * GUIOptions.STEP) // 2 + GUIOptions.MARGIN)

    @staticmethod
    def generate_hexagon_hexagon(sideLength: int) -> SlitherlinkGui:
        size: tuple[int, int] = (2*sideLength-1, 2*sideLength-1)
        points = tuple(
            tuple(PointGui(
                *SlitherlinkGenerator.getHexagonPosition(x, y,
                                                         sideLength % 2 == 0))
                  for x in range(size[0] + 1))
            for y in range(2*size[1] + 2)
        )
        horizontalLines = tuple(
            tuple(
                LineGui((points[2*y + ((x+y) % 2 == 0)][x//2],
                        points[2*y + ((x+1+y) % 2 == 0)][(x+1)//2]))
                for x in range(2*size[0] + 1)
            ) for y in range(size[1] + 1)
        )
        verticalLines = tuple(
            tuple(
                LineGui((points[2*y+1][x], points[2*y+2][x]))
                for x in range(size[0] + 1)
            ) for y in range(size[1])
        )
        fields = [
            FieldGui([
                points[2*y+1][x], points[2*y][x + y %
                                              2], points[2*y + 1][x + 1],
                points[2*y+2][x+1], points[2*y+3][x + y %
                                                  2], points[2*y + 2][x]
            ],
                [
                horizontalLines[y][2*x + y %
                                   2], horizontalLines[y][2*x+1 + y % 2],
                verticalLines[y][x+1], horizontalLines[y+1][2*x+1 + y % 2],
                horizontalLines[y+1][2*x + y % 2], verticalLines[y][x]
            ])
            for y in range(size[1])
            for x in range((abs(sideLength-y-1)+(sideLength % 2 == 0))//2,
                           size[0]-(abs(sideLength-y-1)+(sideLength % 2))//2)
        ]
        return SlitherlinkGui(fields)

    @staticmethod
    def generate_hexagon_rectange(size: tuple[int, int]) -> SlitherlinkGui:
        points = tuple(
            tuple(PointGui(*SlitherlinkGenerator.getHexagonPosition(x, y))
                  for x in range(size[0] + 1))
            for y in range(2*size[1] + 2)
        )
        horizontalLines = tuple(
            tuple(
                LineGui((points[2*y + ((x+y) % 2 == 0)][x//2],
                        points[2*y + ((x+1+y) % 2 == 0)][(x+1)//2]))
                for x in range(2*size[0] + 1)
            ) for y in range(size[1] + 1)
        )
        verticalLines = tuple(
            tuple(
                LineGui((points[2*y+1][x], points[2*y+2][x]))
                for x in range(size[0] + 1)
            ) for y in range(size[1])
        )
        fields = [
            FieldGui([
                points[2*y+1][x], points[2*y][x + y %
                                              2], points[2*y + 1][x + 1],
                points[2*y+2][x+1], points[2*y+3][x + y %
                                                  2], points[2*y + 2][x]
            ],
                [
                horizontalLines[y][2*x + y %
                                   2], horizontalLines[y][2*x+1 + y % 2],
                verticalLines[y][x+1], horizontalLines[y+1][2*x+1 + y % 2],
                horizontalLines[y+1][2*x + y % 2], verticalLines[y][x]
            ])
            for y in range(size[1])
            for x in range(size[0])
        ]
        return SlitherlinkGui(fields)
