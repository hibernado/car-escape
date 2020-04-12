class Colour:
    def __init__(self, rgb):
        self.rgb = rgb

    def __eq__(self, other):
        return other.rgb == self.rgb
