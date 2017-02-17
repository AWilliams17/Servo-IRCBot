def add2toin(num):
    try:
        return int(num) + 2
    except ValueError:
        return "Argument must be a valid integer."
