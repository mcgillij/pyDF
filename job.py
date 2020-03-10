class Job(object):
    """ Job class, generic class for a job """
    def __init__(self, name, move, dest):
        self.name = name
        self.move = move
        self.dest = dest
    def __repr__(self):
        return self.name
