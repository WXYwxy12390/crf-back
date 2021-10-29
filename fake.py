def format_TNM(stage):
    if not stage:
        return '/'
    stage_str = str(stage)
    split_list = stage_str.split(',')
    split_list[0] = 'T:' + split_list[0]
    split_list[1] = 'N:' + split_list[1]
    split_list[2] = 'M:' + split_list[2]
    value = split_list[0] + ',' + split_list[1] + ',' + split_list[2]
    return value


if __name__ == '__main__':
    x = format_TNM('1b,2a,c')
    print(x)
