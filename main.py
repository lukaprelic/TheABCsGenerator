import glob
import string
import offsets
from string import ascii_lowercase

from PIL import Image, ImageOps


def generateAll():
    for index, letter2 in enumerate(ascii_lowercase):
        letter1 = 'A'
        letter2 = letter2.upper()
        letter3 = 'C'
        # print(letter2)
        font = 'Amber Sans Serif'
        hatOffsets = offsets.Offsets('letterHatOffsets.csv')
        hatOffsetsForLetter = hatOffsets.getOffsetsForFontLetter(font, letter2)
        generateImage(id=index,
                      hatoffsets=hatOffsetsForLetter,
                      font=font,
                      backgroundPath='Backgrounds/Desert.png',
                      borderColour='white',
                      letter1Path=('Letters/%s/SaA %s.png' % (font, letter1)),
                      letter2Path=('Letters/%s/SaA %s.png' % (font, letter2)),
                      letter3Path=('Letters/%s/SaA %s.png' % (font, letter3)),
                      hatPath='Hats/Gold.png',
                      addBorder=False)


def walkdir():
    txtfiles = []
    for file in glob.glob("Letters\\*\\*.png", recursive=True):
        txtfiles.append(file)
    print(txtfiles)


def generateImage(id: int, hatoffsets, font, backgroundPath: string, borderColour: string,
                  letter1Path: string, letter2Path: string,
                  letter3Path: string, hatPath: string, addBorder: bool) -> None:
    img = Image.open(fp=backgroundPath)
    if addBorder is True:
        img = addBorder(borderColour, img)
    width, height = img.size
    letter1 = Image.open(fp=letter1Path)
    letterWidth, letterHeight = letter1.size
    letter2 = Image.open(fp=letter2Path)
    letter3 = Image.open(fp=letter3Path)
    hat = getHatImage(hatPath)
    # needed because the letter sprites are not centered
    letterYOffsetLower = 50
    letterxCoordoffset = 12
    (hatxOffsetToLetter, hatyOffset, hatScalar, hatRotation) = hatoffsets
    print('offset:', (hatxOffsetToLetter, hatyOffset, hatScalar, hatRotation))
    letterPasteHeight = int(height / 2) - int(letterHeight / 2) + letterYOffsetLower
    horizontalLetterWidth = int(width / 3 - letterWidth / 2)
    letter1xCoord = int(width / 3 - letterWidth) + letterxCoordoffset
    letter2xCoord = int(width / 3 * 2 - letterWidth) + letterxCoordoffset
    letter3xCoord = int(width / 3 * 3 - letterWidth) + letterxCoordoffset
    print((hat.size[0] * hatScalar, hat.size[1] * hatScalar))
    #change default hat size here
    hat = hat.resize(map(int, (hat.size[0] * hatScalar * 0.85, hat.size[1] * hatScalar * 0.85)))
    hat = hat.rotate(hatRotation)
    img.paste(letter1, (letter1xCoord, letterPasteHeight), letter1)
    img.paste(letter2, (letter2xCoord, letterPasteHeight), letter2)
    img.paste(letter3, (letter3xCoord, letterPasteHeight), letter3)
    #change default hat x coord
    hatxCoord = letter2xCoord + letterxCoordoffset + hatxOffsetToLetter - 60
    # change default hat y coord
    hayyCoord = 160 + hatyOffset
    img.paste(hat, (hatxCoord, hayyCoord), hat)
    finalImageFileName = "Generated/%d ABCs %s%s%s.png" % \
                         (id, letter1Path[-5], letter2Path[-5], letter3Path[-5])
    print("generated image: ", finalImageFileName)
    img.save(finalImageFileName, compress_level=1)
    # img.show(img)


# increase size to allow for no rotation cuttofs
def getHatImage(hatPath):
    hat = Image.open(fp=hatPath)
    (hatWidth, hatHeight) = hat.size
    print(hatWidth, hatHeight)
    hatLargeCanvas = Image.new(mode='RGBA', size=(int(hatWidth * 1.3), int(hatWidth * 1.3)))
    #hatLargeCanvas = ImageOps.expand(hatLargeCanvas, border=2, fill='black')
    hatxycoord = (int(hatWidth * (0.3 / 2 + 1) - hatWidth),
                  int(hatHeight * (0.3 / 2 + 1) - hatHeight) - 35)
    print(hatxycoord)
    hatLargeCanvas.paste(hat, hatxycoord)
    return hatLargeCanvas


def addBorder(borderColour, img):
    img = ImageOps.expand(img, border=10, fill=borderColour)
    return img


if __name__ == '__main__':
    generateAll()
