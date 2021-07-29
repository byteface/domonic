"""
    domonic.d3.polygon
    ====================================

"""

from domonic.javascript import Math, Array

def polygonArea(polygon):
    i = -1
    n = len(polygon)
    a = 0
    b = polygon[n - 1]
    area = 0

    while i < n:
        a = b
        b = polygon[i]
        area += a[1] * b[0] - a[0] * b[1]
        i+=1

    return area / 2


def polygonCentroid(polygon):
    i = -1
    n = len(polygon)
    x = 0
    y = 0
    a = 0
    b = polygon[n - 1]
    c = 0
    k = 0
    while i < n:
        a = b
        b = polygon[i]
        c = a[0] * b[1] - b[0] * a[1]
        k += c
        x += (a[0] + b[0]) * c
        y += (a[1] + b[1]) * c
        i+=1

    k *= 3
    return [x / k, y / k]


def cross(a, b, c):
    """[Returns the 2D cross product of AB and AC vectors, i.e., the z-component of
        the 3D cross product in a quadrant I Cartesian coordinate system (+x is
        right, +y is up). Returns a positive value if ABC is counter-clockwise,
        negative if clockwise, and zero if the points are collinear.]

    Args:
        a ([type]): [description]
        b ([type]): [description]
        c ([type]): [description]

    Returns:
        [type]: [description]
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def lexicographicOrder(a, b, *args):
    return a[0] - b[0] or a[1] - b[1]


def computeUpperHullIndexes(points):
    """[Computes the upper convex hull per the monotone chain algorithm.
        Assumes points.length >= 3, is sorted by x, unique in y.
        Returns an array of indices into points in left-to-right order.]

    Args:
        points ([type]): [description]
    """
    n = len(points)
    indexes = [0, 1]
    size = 2
    for i in range(2, n):
        while (size > 1 and cross(points[indexes[size - 2]], points[indexes[size - 1]], points[i]) <= 0):
            size -= 1
        size += 1
        indexes[size] = i

    return Array(indexes).slice(0, size)  # remove popped points


def polygonHull(points):

    n = len(points)
    if n < 3:
        return None

    sortedPoints = []
    flippedPoints = []

    print(points)

    for i in range(0, n):
        print( points[i][0], points[i][1], i)
        sortedPoints.append([points[i][0], points[i][1], i])

    print(sortedPoints)

    sortedPoints = Array(sortedPoints).sort(lexicographicOrder)

    for i in range(0, n):
        flippedPoints[i] = [sortedPoints[i][0], -sortedPoints[i][1]]

    upperIndexes = computeUpperHullIndexes(sortedPoints)
    lowerIndexes = computeUpperHullIndexes(flippedPoints)

    # Construct the hull polygon, removing possible duplicate endpoints.
    skipLeft = lowerIndexes[0] == upperIndexes[0]
    skipRight = lowerIndexes[len(lowerIndexes) - 1] == upperIndexes[len(upperIndexes) - 1]
    hull = []

    # Add upper hull in right-to-l order.
    # Then add lower hull in left-to-right order.
    i = len(upperIndexes)
    while i >= 0:
        hull.append(points[sortedPoints[upperIndexes[i]][2]])
        i -= 1

    i = skipLeft
    while i < len(lowerIndexes) - skipRight:
        hull.append(points[sortedPoints[lowerIndexes[i]][2]])
        i += 1

    return hull


def polygonContains(polygon, point):
    n = len(polygon)
    p = polygon[n - 1]
    x = point[0]
    y = point[1]
    x0 = p[0]
    y0 = p[1]
    x1 = 0
    y1 = 0
    inside = False
    for i in range(0, n):
        p = polygon[i]
        x1 = p[0]
        y1 = p[1]
        if (((y1 > y) != (y0 > y)) and (x < (x0 - x1) * (y - y1) / (y0 - y1) + x1)):
            inside = not inside
        x0 = x1
        y0 = y1
    return inside


def polygonLength(polygon):
    i = -1
    n = len(polygon)
    b = polygon[n - 1]
    xa = 0
    ya = 0
    xb = b[0]
    yb = b[1]
    perimeter = 0
    while i < n:
        xa = xb
        ya = yb
        b = polygon[i]
        xb = b[0]
        yb = b[1]
        xa -= xb
        ya -= yb
        perimeter += Math.hypot(xa, ya)
        i += 1
    return perimeter
