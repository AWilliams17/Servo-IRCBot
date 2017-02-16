def add2toin(num):
    try:
        return int(num) + 2
    except ValueError:
        raise Exception("Invalid entry.")