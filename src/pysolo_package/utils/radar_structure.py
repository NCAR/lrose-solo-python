class RadarData:
    """ This object contains fields 'data' and 'mask' of list types"""
    def __init__(self, data, mask, changes):
        self.data = data
        self.mask = mask
        self.changes = changes