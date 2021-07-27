my_dict = {
    "apple" : 4,
    "banana" : 9,
    "red-cherry": 12
}


def print_dict(**kargs):
    print(**kargs)


print_dict(**my_dict)