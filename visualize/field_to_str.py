def field_to_str(battlefield):
    """
    dict[(int, int) : None or bool] -> str

    converts dictionary - battlefield representation to string
    and returns this string

    for more information about input and output format
    read read_field.py -> read_field() documentation
    """
    convert = {None: ' ', True: 'X', False: '*'}
    symbols = ''
    for cell in sorted(battlefield.keys()):
        symbols += convert[battlefield[cell]]
    rows = []
    for i in range(10):
        rows.append(symbols[i * 10: i * 10 + 10])
    return '\n'.join(rows)
