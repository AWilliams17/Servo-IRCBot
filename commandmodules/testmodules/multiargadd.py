def add_multi_args(num1, num2, num3):
    try:
        return int(num1) + int(num2) + int(num3)
    except ValueError:
        return "Arguments must be valid integers."
