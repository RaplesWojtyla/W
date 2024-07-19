import basic

while True:
    inp = input('W++> ')
    res, error = basic.run("<stdin>", inp)

    if error:
        print(error.str_error())
    else:
        print(res)
