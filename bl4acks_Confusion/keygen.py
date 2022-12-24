nice_one = [0x4e, 0x69, 0x63, 0x65, 0x4f, 0x6e, 0x65, 0x21, 0x2d, 0x5f]

username = 'abcde'
username_len = len(username)

passwords_to_enter = []

for num in nice_one:
    xor_with_size = hex(num ^ username_len)
    xor_result_in_decimal = int(xor_with_size, base=16)
    print(xor_result_in_decimal)
