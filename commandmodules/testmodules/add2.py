def add2_to_in(num):
    try:
        return int(num) + 2
    except ValueError:
        return "Argument must be a valid integer."
