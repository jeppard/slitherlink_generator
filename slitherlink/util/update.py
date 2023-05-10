
from slitherlink.model.error import UnsolvableError
from slitherlink.model.field import Field
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point
from slitherlink.model.slitherlink import Slitherlink
from slitherlink.util.filter import filterFieldByLine, filterLineByPoint, filterLineByState


def updateLineState(line: Line, state: LineState,
                    slitherlink: Slitherlink) -> list[Line]:
    updated: list[Line] = [line]
    line.state = state
    for point in line.points:
        updated += updatePoint(point, slitherlink)
    for field in filterFieldByLine(slitherlink.fieldlist, line):
        updated += field.update()
    return updated


def updatePoint(point: Point, slitherlink: Slitherlink) -> list[Line]:
    lines: list[Line] = [line for line in filterLineByPoint(
        slitherlink.linelist, point)]
    updated: list[Line] = []
    numSet = sum(1 for _ in filterLineByState(lines, LineState.SET))
    numUnknown = sum(1 for _ in filterLineByState(lines, LineState.UNKNOWN))
    if numSet > 2:
        raise UnsolvableError(
            f"To many Lines set at Point ({point.x},{point.y})")
    if numSet == 1 and numUnknown == 0:
        raise UnsolvableError(
            f"Not enough Lines set at Point ({point.x},{point.y})")
    if numSet == 2:
        for line in filterLineByState(lines, LineState.UNKNOWN):
            updated += updateLineState(line, LineState.UNSET, slitherlink)
    if numUnknown != 1:
        return updated
    if numSet == 1:
        for line in lines:
            if line.state == LineState.UNKNOWN:
                updated += updateLineState(line, LineState.SET, slitherlink)
    else:
        for line in filterLineByState(lines, LineState.UNKNOWN):
            updated += updateLineState(line, LineState.UNSET, slitherlink)
    return updated


def updateField(field: Field, slitherlink: Slitherlink) -> list[Line]:
    updated: list[Line] = []
    if field.number is None:
        return updated  # No information to be gained
    numSet = sum(1 for _ in filterLineByState(field.linelist,
                                              LineState.SET))
    numUnknown = sum(1 for _ in filterLineByState(field.linelist,
                                                  LineState.UNKNOWN))
    if numSet + numUnknown < field.number:
        raise UnsolvableError(f"Not enough Lines can be set on field {field}")
    if numSet > field.number:
        raise UnsolvableError(f"To much Lines set on field {field}")
    if numSet == field.number:
        for line in filterLineByState(field.linelist, LineState.UNKNOWN):
            updated += updateLineState(line, LineState.UNSET, slitherlink)
    elif numSet + numUnknown == field.number:
        for line in filterLineByState(field.linelist, LineState.UNKNOWN):
            updated += updateLineState(line, LineState.SET, slitherlink)
    return updated
