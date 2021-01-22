"""Convert the Euler angles convention."""


from sympy import pi, sin, cos, acos, asin, atan2, Matrix
from math import radians, degrees

dec_num = 4


def abc2oat(a, b, c, input_deg=False, output_deg=False):

    if input_deg:
        a = radians(a)
        b = radians(b)
        c = radians(c)

    rot_x = Matrix([[1, 0, 0], [0, cos(a), -sin(a)], [0, sin(a), cos(a)]])
    rot_y = Matrix([[cos(b), 0, sin(b)], [0, 1, 0], [-sin(b), 0, cos(b)]])
    rot_z = Matrix([[cos(c), -sin(c), 0], [sin(c), cos(c), 0], [0, 0, 1]])

    rot_zyx = rot_z * rot_y * rot_x

    if (rot_zyx[8] > -1) and (rot_zyx[8] < 1):
        azimuth = acos(rot_zyx[8])
        orientation = atan2(rot_zyx[5] / sin(azimuth), rot_zyx[2] / sin(azimuth))
        tool = atan2(rot_zyx[7] / sin(azimuth), -rot_zyx[6] / sin(azimuth))
        # azimuth2 = acos(-rot_zyx[8])  # cos(-alpha) = cos(alpha)
        # orientation2 = atan2(rot_zyx[5]/sin(azimuth2), rot_zyx[2]/sin(azimuth2))
        # tool2 = atan2(rot_zyx[7]/sin(azimuth2), -rot_zyx[6]/sin(azimuth2))

    elif rot_zyx[8] <= -1:  # gimbal lock, calculate for Z3 = 0; Y2 = pi
        azimuth = pi
        tool = 0
        orientation = atan2(rot_zyx[3], -rot_zyx[0]) + tool
        # azimuth2 = -pi
        # tool2 = tool
        # orientation2 = orientation

    else:  # gimbal lock, calculate for Z3 = 0; Y2 = 0
        azimuth = 0
        tool = 0
        orientation = atan2(rot_zyx[3], rot_zyx[0]) - tool
        # azimuth2 = azimuth
        # tool2 = tool
        # orientation2 = orientation

    if output_deg:
        oat_angles = (
            round(degrees(orientation), dec_num),
            round(degrees(azimuth), dec_num),
            round(degrees(tool), dec_num),
        )
    else:
        oat_angles = (
            round(orientation, dec_num),
            round(azimuth, dec_num),
            round(tool, dec_num),
        )
    # print(orientation2, azimuth2, tool2)
    return oat_angles, rot_zyx


def oat2abc(orientation, azimuth, tool, input_deg=False, output_deg=False):

    if input_deg:
        orientation = radians(orientation)
        azimuth = radians(azimuth)
        tool = radians(tool)

    rot_z = Matrix(
        [
            [cos(orientation), -sin(orientation), 0],
            [sin(orientation), cos(orientation), 0],
            [0, 0, 1],
        ]
    )
    rot_y = Matrix(
        [[cos(azimuth), 0, sin(azimuth)], [0, 1, 0], [-sin(azimuth), 0, cos(azimuth)]]
    )
    rot_zz = Matrix([[cos(tool), -sin(tool), 0], [sin(tool), cos(tool), 0], [0, 0, 1]])

    rot_zyz = rot_z * rot_y * rot_zz

    if (rot_zyz[6] > -1) and (rot_zyz[6] < 1):
        b = -asin(rot_zyz[6])
        c = atan2(rot_zyz[3] / cos(b), rot_zyz[0] / cos(b))
        a = atan2(rot_zyz[7] / cos(b), rot_zyz[8] / cos(b))

    elif rot_zyz[6] <= -1:  # gimbal lock, calculate for c = 0; b = pi/2
        b = pi / 2
        c = 0
        a = atan2(rot_zyz[1], rot_zyz[4]) - c

    else:  # gimbal lock, calculate for c = 0; b = -pi/2
        b = -pi / 2
        c = 0
        a = -atan2(rot_zyz[1], rot_zyz[4]) - c

    if output_deg:
        abc_angles = (
            round(degrees(a), dec_num),
            round(degrees(b), dec_num),
            round(degrees(c), dec_num),
        )
    else:
        abc_angles = (round(a, dec_num), round(b, dec_num), round(c, dec_num))
    return abc_angles, rot_zyz


if __name__ == "__main__":
    print(abc2oat(1.047200, 1.047200, 0.7853976)[0])
    print(oat2abc(-0.3217524, 1.318118, 0.4636459)[0])
    print("========================================")
    print(abc2oat(90.0, 65.0, 15.0, True, True)[0])
    print(oat2abc(-75.0, 90.0, 25.0, True, True)[0])
    print("========================================")
    print(oat2abc(90.0, 65.0, 15.0, True, True)[0])
    print(abc2oat(29.031993, 61.095444, 122.375588, True, True)[0])
    print("========================================")
    print(oat2abc(95.0, 75.0, -15.0, True, False)[0])
    print(abc2oat(-0.7681, 1.2027, 0.8553, False, True)[0])
    print("========================================")
    print(oat2abc(-15, 180, 15, True, True))
    print()
    print(abc2oat(180.0, 0.0, 150.0, True, True))
    print("========================================")
    print(oat2abc(-15, 90, 15, True, True))
    print()
    print(abc2oat(90.0, 75.0, 75.0, True, True))
    print("========================================")
    print(oat2abc(-89, 90, 15, True, True))
    print()
    print(abc2oat(90.0, 75.0, 1.0, True, True))
