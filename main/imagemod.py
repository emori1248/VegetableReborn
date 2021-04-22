from PIL import Image, ImageFont, ImageDraw 
import random, os

async def addCenteredTextToImage(content):
    # Grab a random image from the directory
    
    imagedir = random.choice(os.listdir("img"))
    image = Image.open("img/" + imagedir)
    
    font_size = int( (image.width) / len(content) )

    title_font = ImageFont.truetype('font/comic.ttf', font_size)
    image_editable = ImageDraw.Draw(image)

    
    starting_x = 10

    #starting_y = 10
    starting_y = (image.height / 2 - 50)
    
    image_editable.text((starting_x, starting_y), content, (15, 15, 15), font=title_font)
    image_editable.text((starting_x, starting_y), content, (15, 15, 15), font=title_font)
    image.save("img/result.jpg")
    return "img/result.jpg"

async def deleteResult():
    os.remove("img/result.jpg")

