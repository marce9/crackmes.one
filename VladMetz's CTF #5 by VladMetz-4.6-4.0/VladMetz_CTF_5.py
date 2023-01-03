import random


is_valid_char = lambda num: True if (isinstance(num, int) and (
            ('0' <= chr(num) <= '9') or ('A' <= chr(num) <= 'Z') or ('a' <= chr(num) <= 'z'))) else False

# ************************** SECOND PHASE (Random) **************************
'''
xmm0 = pass[1]
xmm1 = pass[6]
xmm2 = (pass[6] * pass[2]) - (pass[5] / 2)^2
xmm3 = pass[5] / 2
xmm4 = pass[4] / 2
xmm5 = pass[3] * 0.5
'''


def get_parity(n):
    bit = 0
    num_bits = 0
    while n:
        bitmask = 1 << bit
        bit += 1
        if n & bitmask:
            num_bits += 1
        n &= ~bitmask
    return (num_bits % 2) ^ 1


def get_valid_char_only_letters():
    # omitting numbers since it takes a long time to search when numbers are included
    result = random.randint(65, 123)
    while not is_valid_char(result):
        result = random.randint(65, 123)
    return result


while True:
    pass_1 = get_valid_char_only_letters()
    pass_2 = get_valid_char_only_letters()
    pass_3 = get_valid_char_only_letters()
    pass_4 = get_valid_char_only_letters()
    pass_5 = get_valid_char_only_letters()
    pass_6 = get_valid_char_only_letters()

    # set XMM registers
    xmm0 = pass_1
    xmm1 = pass_6
    xmm2 = (pass_6 * pass_2) - pow((pass_5 / 2), 2)
    xmm3 = pass_5 / 2
    xmm4 = pass_4 / 2
    xmm5 = pass_3 * 0.5

    # calculations
    xmm1 *= xmm5
    xmm2 *= xmm0
    xmm0 = xmm3
    xmm0 *= xmm4
    xmm3 *= xmm5
    xmm1 -= xmm0
    xmm0 = pass_2
    xmm1 *= xmm5
    xmm0 *= xmm4
    xmm2 -= xmm1
    xmm3 -= xmm0
    xmm3 *= xmm4
    xmm2 += xmm3
    xmm0 = xmm2

    # compare xmm0 with 49332CACh = 733898.75 ("ucomiss" command)
    if xmm0 > 733898.75:
        ZF = 0
        PF = 0
        CF = 0
    elif xmm0 < 733898.75:
        ZF = 0
        PF = 0
        CF = 1
    else:
        ZF = 1
        PF = 0
        CF = 0
    eax = int((pass_6 * pass_2) - pow((pass_5 / 2), 2))
    AH = int(eax >> 8)  # remove right byte
    AH = int(AH & 255)  # remove remaining bytes (2 most significant) - bitwise AND with 11111111
    AL = int(eax & 255)  # bitwise AND with 11111111

    # set AH bits according to ZF,PF,CF - "lahf" instruction
    if ZF == 1:
        AH = AH | 64  # 01 00 00 00
    else:
        AH = AH & 191  # 10 11 11 11
    if PF == 1:
        AH = AH | 4  # 00 00 01 00
    else:
        AH = AH & 251  # 11 11 10 11
    if CF == 1:
        AH = AH | 1  # 00 00 00 01
    else:
        AH = AH & 254  # 11 11 11 10
    AH_test_result = AH & 68  # test ah, 44h
    AH_parity = get_parity(AH_test_result)
    if AH_parity < 1:
        # success!        print(AH)
        print('pass[0] = \'{0}\'\n'
              'pass[1] = \'{1}\'\n'
              'pass[2] = \'{2}\'\n'
              'pass[3] = \'{3}\'\n'
              'pass[4] = \'{4}\'\n'
              'pass[5] = \'{5}\'\n\n'.format(chr(pass_1),
                                             chr(pass_2),
                                             chr(pass_3),
                                             chr(pass_4),
                                             chr(pass_5),
                                             chr(pass_6)))
        break


# ************************** FIRST PHASE (Deterministic) **************************


# (pass[8] * pass[11]) + (pass[10] * (pass[12] + pass[7])) == 9AF2h
# x = pass[8] * pass[11]
# y = pass[10] * (pass[12] + pass[7])
# x + y = 9AF2h
# a = pass[10]
# b = pass[12] + pass[7]
# a * b = y


condition_num = 0x9AF2
x = 2

while x <= condition_num:
    y = condition_num - x
    # print('{0},{1}'.format(chr(x), chr(y)))
    pass_7 = 0
    pass_8 = 0
    pass_10 = 0
    pass_11 = 0
    pass_12 = 0
    x_divider = ord('0')
    while x_divider <= ord('z'):
        x_division_result = int(x / x_divider) if (x % x_divider == 0) else x / x_divider
        x_condition = (is_valid_char(x_divider) and is_valid_char(x_division_result))
        if not x_condition:
            x_divider += 1
        else:
            pass_8 = x_divider
            pass_11 = x_division_result
            # print('pass[8] = \'{0}\', pass[10] = \'{1}\''.format(chr(x_divider), chr(x_division_result)))
            # found x and y such that (x) is True -> now search for values such that (y) will be True
            y_divider = ord('0')
            while y_divider <= ord('z'):
                y_division_result = int(y / y_divider) if (y % y_divider == 0) else y / y_divider
                y_condition = (is_valid_char(y_divider) and isinstance(y_division_result, int))
                if not y_condition:
                    y_divider += 1
                else:
                    pass_10 = y_divider  # a
                    b_1 = ord('0')
                    while b_1 <= ord('z'):
                        b_2 = y_division_result - b_1
                        a_b_condition = (is_valid_char(b_1) and is_valid_char(b_2))
                        if not a_b_condition:
                            b_1 += 1
                        else:
                            pass_7 = b_1
                            pass_12 = b_2
                            print('pass[7] = \'{0}\'\n'
                                  'pass[8] = \'{1}\'\n'
                                  'pass[9] = \'{2}\'\n'
                                  'pass[10] = \'{3}\'\n'
                                  'pass[11] = \'{4}\'\n'.format(chr(pass_7),
                                                                chr(pass_8),
                                                                chr(pass_10),
                                                                chr(pass_11),
                                                                chr(pass_12)))
                            raise SystemExit
                    y_divider += 1
            x_divider += 1
    x += 1
