import re
from euler import abc2oat
from circular_inter import set_mid_point


def translate(nc_path, as_path, base, tool, rapid_speed, rapid_accuracy, line_speed, line_accuracy,
              circular_speed, circular_accuracy, options_speed, options_base):

    path_nc = nc_path
    path_nc_clean = nc_path
    path_as = as_path

    flag_g00, flag_g01, flag_g02, flag_g03, flag_g90, flag_g91 = False, False, False, False, False, False
    x, y, z, a, b, c, ix, jy = 0, 0, 0, 0, 0, 0, 0, 0
    change = False
    point = (0, 0, 0, 0, 0, 0)
    file = open(path_nc, "r")
    code_nc = file.read()
    file.close()
    pattern = re.compile(r'\s?(([GXYZABCIJKF]-?\d+[\s|.]?\d*)\s)+')
    matches = pattern.finditer(code_nc)
    clean_code = ''
    for match in matches:
        clean_code += match.group(0)[1:] if match.group(0)[-1] == '\n' else (match.group(0)[1:] + '\n')
    file = open(path_nc_clean[:-3] + '_clean.txt', 'w')
    file.writelines(clean_code + '\n')
    file.close()

    as_code = open(path_as, 'w')
    w_beg = as_path.rfind("/") + 1
    as_code.writelines(f'.PROGRAM {path_as[w_beg:]}' + '\n')
    as_code.writelines(f'TOOL TRANS{tool} \n')
    # as_code.writelines(f'LMOVE {base} \n')

    for line in clean_code.splitlines():
        for word in line.split():
            if word == 'G90':
                flag_g90 = True
                flag_g91 = False
            elif word == 'G91':
                flag_g91 = True
                flag_g90 = False
            elif word.startswith('F') and options_speed == 1:
                f = float(word[1:])
                as_code.writelines(f'SPEED {f}' + ' MM/S' + '\n')
            elif word == 'G00' or word == 'G0':
                flag_g00 = True
                flag_g01, flag_g02, flag_g03 = False, False, False
                as_code.writelines(f'ACCURACY {rapid_accuracy}' + '\n')
                if options_speed == 0:
                    as_code.writelines(f'SPEED {rapid_speed}' + '\n')
            elif word == 'G01':
                flag_g01 = True
                flag_g00, flag_g02, flag_g03 = False, False, False
                as_code.writelines(f'ACCURACY {line_accuracy}' + '\n')
                if options_speed == 0:
                    as_code.writelines(f'SPEED {line_speed}' + '\n')
            elif word == 'G02':
                flag_g02 = True
                flag_g00, flag_g01, flag_g03 = False, False, False
                as_code.writelines(f'ACCURACY {circular_accuracy}' + '\n')
                if options_speed == 0:
                    as_code.writelines(f'SPEED {circular_speed}' + '\n')
            elif word == 'G03':
                flag_g03 = True
                flag_g00, flag_g01, flag_g02 = False, False, False
                as_code.writelines(f'ACCURACY {circular_accuracy}' + '\n')
                if options_speed == 0:
                    as_code.writelines(f'SPEED {circular_speed}' + '\n')

            if flag_g90:
                if word.startswith('X'):
                    x = float(word[1:])
                    change = True
                elif word.startswith('Y'):
                    y = float(word[1:])
                    change = True
                elif word.startswith('Z'):
                    z = float(word[1:])
                    change = True
                elif word.startswith('A'):
                    a = float(word[1:])
                    change = True
                elif word.startswith('B'):
                    b = float(word[1:])
                    change = True
                elif word.startswith('C'):
                    c = float(word[1:])
                    change = True
                if flag_g02 or flag_g03:
                    if word.startswith('I'):
                        ix = float(word[1:])
                        change = True
                    elif word.startswith('J'):
                        jy = float(word[1:])
                        change = True
            if not flag_g90:
                print(' ')

        if change:
            change = False
            old_point = point
            oat_angles = abc2oat(b, a, -c, True, True)[0]
            point = (y, x, -z, oat_angles[0], oat_angles[1], oat_angles[2])
            c_point = (jy, ix)
            if (flag_g00 or flag_g01) and flag_g90:
                as_code.writelines('LMOVE workpiece + TRANS' + str(point) + '\n')
            if (flag_g02 or flag_g03) and flag_g90:
                circle_approx_mode = 'CW' if flag_g02 else 'CCW'
                circle_approx = set_mid_point(old_point, point, c_point, circle_approx_mode)
                as_code.writelines('C1MOVE workpiece + TRANS' + str(circle_approx) + '\n')
                as_code.writelines('C2MOVE workpiece + TRANS' + str(point) + '\n')

    as_code.writelines('.END' + '\n')
    as_code.writelines('.TRANS' + '\n')
    as_code.writelines(f'workpiece {base[1:-1].replace(",", "")}' + '\n')
    as_code.writelines('.END' + '\n')
    as_code.close()
    return None
