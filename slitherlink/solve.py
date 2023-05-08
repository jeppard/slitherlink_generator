from slitherlink.model.slitherlink import Slitherlink


def isSolved(slitherlink: Slitherlink):
    return all(field.isSolved() for field in slitherlink.fieldlist) and \
        all(point.isSolved() for point in slitherlink.points) and \
        slitherlink.hasOnePath()


def isSolvable(slitherlink: Slitherlink):
    return all(field.isSolvable() for field in slitherlink.fieldlist) and \
        all(point.isSolvable() for point in slitherlink.points) and \
        slitherlink.isSolvable()
