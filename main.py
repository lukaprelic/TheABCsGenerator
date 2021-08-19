import string

from PIL import Image, ImageDraw, ImageFont, ImageOps


def generateAll():
    generateImage(backgroundPath='Backgrounds/City.png',
                  borderColour='white',
                  letter1Path='Letters/Amber Calligraphy/CA A.png',
                  letter2Path='Letters/Amber Calligraphy/CA B.png',
                  letter3Path='Letters/Amber Calligraphy/CA C.png',
                  hatPath='Hats/Gold.png',
                  addBorder=False)


def generateImage(backgroundPath: string, borderColour: string,
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
    hat = Image.open(fp=hatPath)
    # needed because the letter sprites are not centered
    letterVerticalOffsetLower = 50
    letterxcoordoffset = 13
    hatxoffset = 5
    letterPasteHeight = int(height / 2) - int(letterHeight / 2) + letterVerticalOffsetLower
    horizontalLetterWidth = int(width / 3 - letterWidth / 2)
    letter1xCoord = int(width / 3 - letterWidth) + letterxcoordoffset
    letter2xCoord = int(width / 3 * 2 - letterWidth) + letterxcoordoffset
    letter3xCoord = int(width / 3 * 3 - letterWidth) + letterxcoordoffset
    img.paste(letter1, (letter1xCoord, letterPasteHeight), letter1)
    img.paste(letter2, (letter2xCoord, letterPasteHeight), letter2)
    img.paste(letter3, (letter3xCoord, letterPasteHeight), letter3)
    img.paste(hat, (horizontalLetterWidth * 2 + letterxcoordoffset + hatxoffset, 130), hat)
    finalImageFileName = "test.png"
    print("generated image: ", finalImageFileName)
    img.save(finalImageFileName, compress_level=0)
    # img.show(img)


def addBorder(borderColour, img):
    img = ImageOps.expand(img, border=10, fill=borderColour)
    return img


if __name__ == '__main__':
    generateAll()
