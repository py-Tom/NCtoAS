"""Convert cirular interpolation."""


from math import pi, sin, cos, atan, sqrt


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def set_angle(x, y):
    if y == 0 and x > 0:
        angle = pi / 2
    elif y == 0 and x < 0:
        angle = 3 * pi / 2
    elif x == 0 and y == 0:
        raise ValueError("(0, 0)")
    else:
        angle = atan(x / y)

    if y < 0:
        angle += pi
    elif x < 0:
        angle += 2 * pi

    angle = angle if angle < 2 * pi else angle % (2 * pi)

    return round(angle, 7)


def set_mid_angle(s_angle, e_angle, mode):
    if s_angle < 0 or e_angle < 0:
        raise ValueError("wrong angles")

    if s_angle >= 2 * pi:
        s_angle %= 2 * pi
    if e_angle >= 2 * pi:
        e_angle %= 2 * pi

    if s_angle == e_angle:
        m_angle = pi + s_angle
    else:
        m_angle = (e_angle - s_angle) / 2 + s_angle

    if (s_angle < e_angle and mode == "CCW") or (s_angle > e_angle and mode == "CW"):
        m_angle += pi

    return round(m_angle, 7)


def set_mid_coord(m_angle, r, x, y):

    m_coord = [round(r * sin(m_angle) + x, 7), round(r * cos(m_angle) + y, 7)]
    return m_coord


def set_mid_point(start_point, end_point, center, mode):
    circle = Coord(start_point[0] + center[0], start_point[1] + center[1])

    start = Coord(start_point[0] - circle.x, start_point[1] - circle.y)
    end = Coord(end_point[0] - circle.x, end_point[1] - circle.y)

    start_angle = set_angle(start.x, start.y)
    end_angle = set_angle(end.x, end.y)
    mid_angle = set_mid_angle(start_angle, end_angle, mode)

    radius = sqrt(center[0] ** 2 + center[1] ** 2)
    m_point = set_mid_coord(mid_angle, radius, circle.x, circle.y)

    middle_point = (
        m_point[0],
        m_point[1],
        start_point[2],
        start_point[3],
        start_point[4],
        start_point[5],
    )
    return middle_point
