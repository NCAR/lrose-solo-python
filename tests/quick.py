def write_eq(show_equal, *args, product = 1):
    equation = ""
    for num in args:
        equation += str(num) + " * "
    equation = equation[:-3]
    if show_equal:
        equation += " = " + str(product)
    return equation

def product(*args):
    product = 1
    for num in args:
        product *= num
    print(write_eq(False, *args, product = product))

product(2, 5, 3)

#    masked(required, required, optional):
#       funct(required, )