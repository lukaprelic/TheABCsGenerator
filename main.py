from PIL import Image, ImageDraw, ImageFont, ImageOps


def run():
    img = Image.open(fp='Backgrounds/City.png')
    img = ImageOps.expand(img, border=10, fill='white')
    width, height = img.size
    letter1 = Image.open(fp='Letters/Amber Calligraphy/CA A.png')
    letter2 = Image.open(fp='Letters/Amber Calligraphy/CA B.png')
    letter3 = Image.open(fp='Letters/Amber Calligraphy/CA C.png')
    hat = Image.open(fp='Hats/Gold.png')
    img.paste(letter1, (0, 350), letter1)
    img.paste(letter2, (350, 350), letter2)
    img.paste(letter3, (700, 350), letter3)
    img.paste(hat, (250, 0), hat)
    fnt = ImageFont.truetype('arial.ttf', 55)
    d = ImageDraw.Draw(img)
    d.text((10, 10), "size:("+str(width)+":"+str(height)+")", font=fnt, fill=(255, 255, 0))
    img.save("test.png")
    #img.show(img)


if __name__ == '__main__':
    run()
