"""
    domonic.d3.polygon
    ====================================

"""

from domonic.javascript import Array, Math


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

def polygonHull(points):

    n = len(points)
    if n < 3:
        return None

    # Convert list to tuples and remove duplicates
    points = [t for t in (set(tuple(i) for i in points))]

    # Sort lexicographically 
    points = sorted(points)

    # Build hulls according to Andrew's monotone chain algorithm
    lowerHull = []
    for p in points:
        while len(lowerHull) >= 2 and cross(lowerHull[-2], lowerHull[-1], p) <=0 :
            lowerHull.pop()
        lowerHull.append(p)

    upperHull = []
    for p in reversed(points):
        while len(upperHull) >= 2 and cross(upperHull[-2], upperHull[-1], p) <= 0:
            upperHull.pop()
        upperHull.append(p)
    
    # Build polygon hull from upper/lower hulls and return to list form
    hull = sorted([list(i) for i in lowerHull[:-1] + upperHull[:-1]])
    
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