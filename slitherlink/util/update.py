
from slitherlink.model.error import UnsolvableError
from slitherlink.solver import isSolvable
from slitherlink.util.filter import filterFieldByLine, \
    filterLineByPoint, filterLineByState
from slitherlink.model.line_state import LineState

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from slitherlink.model.slitherlink import Slitherlink
    from slitherlink.model.field import Field
    from slitherlink.model.line import Line
    from slitherlink.model.point import Point


def setLineState(line: 'Line', state: LineState,
                 slitherlink: 'Slitherlink') -> list['Line']:
    updated: list['Line'] = [line]
    line.state = state
    if state == LineState.UNKNOWN:
        return updated
    for point in line.points:
        updated += updatePoint(point, slitherlink)
    for field in filterFieldByLine(slitherlink.fieldlist, line):
        updated += updateField(field, slitherlink)
    return updated


def setFieldLabel(field: 'Field', label: int, slitherlink: 'Slitherlink'):
    numSetLines = sum(1 for _ in filterLineByState(
        field.linelist, LineState.SET))
    numUnknownLines = sum(1 for _ in filterLineByState(
        field.linelist, LineState.UNKNOWN))
    if numSetLines > label:
        raise UnsolvableError("Label is too low")
    if numSetLines + numUnknownLines < label:
        raise UnsolvableError("Label is too high")
    if field.number is not None:
        raise UnsolvableError("Label is already set")
    updated: list['Line'] = []
    try:
        field.number = label
        updated += updateField(field, slitherlink)
        if isSolvable(slitherlink) is False:
            raise UnsolvableError("Slitherlink is not solvable")
    except UnsolvableError as e:
        field.number = None
        for line in updated:
            line.state = LineState.UNKNOWN
        raise e


def updatePoint(point: 'Point', slitherlink: 'Slitherlink') -> list['Line']:
    lines: list['Line'] = [line for line in filterLineByPoint(
        slitherlink.linelist, point)]
    updated: list['Line'] = []
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
            updated += setLineState(line, LineState.UNSET, slitherlink)
    if numUnknown != 1:
        return updated
    if numSet == 1:
        for line in lines:
            if line.state == LineState.UNKNOWN:
                updated += setLineState(line, LineState.SET, slitherlink)
    else:
        for line in filterLineByState(lines, LineState.UNKNOWN):
            updated += setLineState(line, LineState.UNSET, slitherlink)
    return updated


def updateField(field: 'Field', slitherlink: 'Slitherlink') -> list['Line']:
    updated: list['Line'] = []
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
            updated += setLineState(line, LineState.UNSET, slitherlink)
    elif numSet + numUnknown == field.number:
        for line in filterLineByState(field.linelist, LineState.UNKNOWN):
            updated += setLineState(line, LineState.SET, slitherlink)
    return updated
