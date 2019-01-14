class End:

    def __init__(self):
        pass

    def __repr__(self):
        return 'End'

    def __eq__(self, other):
        if isinstance(other, End):
            return True
        return False
