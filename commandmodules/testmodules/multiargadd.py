def add_multiargs(num1, num2, num3):
    try:
        return int(num1) + int(num2) + int(num3)
    except ValueError:
        raise Exception("Invalid entry.")
