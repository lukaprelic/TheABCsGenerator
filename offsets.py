import os, pandas
from enum import Enum

fontColOffset = {'Serif': 0, 'Sans Serif': 1}


class Offsets:
    def __init__(self, path):
        self.data = pandas.read_csv(path)

    def getOffsetsForFontLetter(self, hat, font, letter):
        d = self.data
        rowIndex = ord(letter) - ord('A')
        fontWithNoColour = ' '.join(font.split(' ')[1:])
        hatxOffset, hatyOffset, hatScalar, rotation = (d[hat + ' ' + fontWithNoColour][rowIndex].split(","))
        hatxOffset, hatyOffset, hatScalar, rotation = \
            int(hatxOffset), int(hatyOffset), float(hatScalar), int(rotation)
        return hatxOffset, hatyOffset, hatScalar, rotation