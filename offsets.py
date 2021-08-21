import os, pandas


class Offsets:
    def __init__(self, path):
        self.data = pandas.read_csv(path)

    def getOffsetsForFontLetter(self, font, letter):
        d = self.data
        rowIndex = ord(letter) - ord('A')
        hatxOffset, hatyOffset, hatScalar, rotation = (d[font][rowIndex].split(","))

        hatxOffset, hatyOffset, hatScalar, rotation = \
            int(hatxOffset), int(hatyOffset), float(hatScalar), int(rotation)
        return hatxOffset, hatyOffset, hatScalar, rotation
