class tee:
    def __init__(self):
        pass

    def nn(self):
        raise NotImplementedError


class coffee(tee):
    def __init__(self):
        pass

    def nn(self):
        print(1)


class coffee2(tee):
    def __init__(self):
        pass

    def nn(self):
        print(2)


coffee().nn()
coffee2().nn()

l=coffee2()
l.nn()
l.nn = coffee().nn

l.nn()

coffee2().nn()
