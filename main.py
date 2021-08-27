import string
from pathlib import Path

import pandas

import generator
import offsets
from string import ascii_lowercase

from PIL import Image, ImageOps


def generateAlphabet():
    for index, letter2 in enumerate(ascii_lowercase):
        letter1 = 'A'
        letter2 = letter2.upper()
        letter3 = 'C'
        font = 'Sans Serif Amber'
        hat = 'Bubblegum'
        hatOffsets = offsets.Offsets('letterHatOffsets.csv')
        generateImage(id=index,
                      hatOffsets=hatOffsets,
                      fontAndColourComb=font,
                      backgroundPath='Backgrounds/Desert.png',
                      borderColour='white',
                      letter1Char=letter1,
                      letter2Char=letter2,
                      letter3Char=letter3,
                      hat=hat,
                      addBorder=False)


def generateAll(countstart, count):
    Path("Generated").mkdir(parents=True, exist_ok=True)
    hatOffsets = offsets.Offsets('letterHatOffsets.csv')
    csvRows = []

    for index in range(countstart, countstart + count):
        background, letter1, letter2, letter3, fontAndColourComb, hat = generator.generateCombination()
        letterPermutation = letter1 + letter2 + letter3
        font = ' '.join(fontAndColourComb.split(' ')[:-1])
        fontColour = fontAndColourComb.split(' ')[-1]
        special = ''
        isNoHatFont = any(noHatFonts in font for noHatFonts in ['Calligraphy'])
        if isNoHatFont:
            hat = 'None'
        csvRows.append(list((index, background, font,
                             fontAndColourComb, fontColour, hat,
                             letter1, letter2, letter3, letterPermutation, special)))
        print(
            (index, background, font, fontAndColourComb, fontColour, hat, letter1,
             letter2, letter3, letterPermutation, special))
        generateImage(id=index,
                      hatOffsets=hatOffsets,
                      fontAndColourComb=fontAndColourComb,
                      backgroundPath='Backgrounds/%s.png' % background,
                      borderColour='white',
                      letter1Char=letter1,
                      letter2Char=letter2,
                      letter3Char=letter3,
                      hat=hat,
                      addBorder=False)
    csv = pandas.DataFrame(csvRows,
                           columns=['Id', 'Background', 'Font', 'Font & Colour Combination',
                                    'Font Colour', 'Hat', 'Letter1', 'Letter2',
                                    'Letter3', 'Letter Permutation', 'Special'])
    csv.to_csv('Generated/metadata.csv', index=False)


def generateImage(id: int, hatOffsets, fontAndColourComb, backgroundPath: string, borderColour: string,
                  letter1Char: string, letter2Char: string,
                  letter3Char: string, hat: string, addBorder: bool) -> None:
    img = Image.open(fp=backgroundPath)
    if addBorder is True:
        img = addBorder(borderColour, img)
    width, height = img.size
    letter1Path = ('Letters/%s/%s.png' % (fontAndColourComb, letter1Char))
    letter2Path = ('Letters/%s/%s.png' % (fontAndColourComb, letter2Char))
    letter3Path = ('Letters/%s/%s.png' % (fontAndColourComb, letter3Char))
    letter1 = Image.open(fp=letter1Path)
    letterWidth, letterHeight = letter1.size
    letter2 = Image.open(fp=letter2Path)
    letter3 = Image.open(fp=letter3Path)
    # needed because the letter sprites are not centered
    letterYOffsetLower = 50
    letterxCoordoffset = 12
    letterPasteyCoord = int(height / 2) - int(letterHeight / 2) + letterYOffsetLower
    letter1xCoord = int(width / 3 - letterWidth) + letterxCoordoffset
    letter2xCoord = int(width / 3 * 2 - letterWidth) + letterxCoordoffset
    letter3xCoord = int(width / 3 * 3 - letterWidth) + letterxCoordoffset
    img.paste(letter1, (letter1xCoord, letterPasteyCoord), letter1)
    img.paste(letter2, (letter2xCoord, letterPasteyCoord), letter2)
    img.paste(letter3, (letter3xCoord, letterPasteyCoord), letter3)
    if hat != 'None':
        hatOffsetsForLetter = hatOffsets.getOffsetsForFontLetter(hat, fontAndColourComb, letter2Char)
        addHat(hat, hatOffsetsForLetter, img, letter2xCoord, letterxCoordoffset)
    finalImageFileName = "Generated/%d ABCs %s%s%s %s.png" % \
                         (id, letter1Path[-5], letter2Path[-5], letter3Path[-5], hat)
    print("generated image: ", finalImageFileName)
    img.save(finalImageFileName, compress_level=0)


def addHat(hatName, hatoffsets, img, letter2xCoord, letterxCoordoffset):
    hat = getHatImage(hatName)
    (hatxOffsetToLetter, hatyOffset, hatScalar, hatRotation) = hatoffsets
    print('csv offset:', (hatxOffsetToLetter, hatyOffset, hatScalar, hatRotation))
    # change default hat size here
    hat = hat.resize(map(int, (hat.size[0] * hatScalar * 0.85, hat.size[1] * hatScalar * 0.85)))
    hat = hat.rotate(hatRotation)
    # change default hat x coord
    hatxCoord = letter2xCoord + letterxCoordoffset + hatxOffsetToLetter - 60
    # change default hat y coord
    hatyCoord = 160 + hatyOffset
    # print((hat.size[0] * hatScalar, hat.size[1] * hatScalar))
    img.paste(hat, (hatxCoord, hatyCoord), hat)


# increase size to allow for no rotation cuttoffs
def getHatImage(hatName):
    hatPath = ('Hats/%s.png' % (hatName))
    hat = Image.open(fp=hatPath)
    (hatWidth, hatHeight) = hat.size
    hatLargeCanvas = Image.new(mode='RGBA', size=(int(hatWidth * 1.3), int(hatWidth * 1.3)))
    hatxyCoord = (int(hatWidth * (0.3 / 2 + 1) - hatWidth),
                  int(hatHeight * (0.3 / 2 + 1) - hatHeight) - 35)
    hatLargeCanvas.paste(hat, hatxyCoord)
    return hatLargeCanvas


def addBorder(borderColour, img):
    img = ImageOps.expand(img, border=10, fill=borderColour)
    return img


if __name__ == '__main__':
    # generateAlphabet()
    generateAll(51, 200)
