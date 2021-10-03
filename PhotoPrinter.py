import cv2
from PIL import Image
from PIL.ExifTags import TAGS
import math
import os



def show(img):
    cv2.imshow("Image Test",img)
    cv2.waitKey(0)
    #closing all open windows
    cv2.destroyAllWindows()

def addBorder(img):
    color = [255, 255, 255]
    if img.shape[1] >= img.shape[0]:
        squareSize = round(img.shape[1]+1000, -3)
    else:
        squareSize = round(img.shape[0]+1000, -3)
    top = int((squareSize-img.shape[0])/2)
    bottom = int((squareSize-img.shape[0])/2)
    left = int((squareSize-img.shape[1])/2)
    right = int((squareSize-img.shape[1])/2)
    bottomBorder = top + img.shape[0]

    img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return img_with_border, bottomBorder

def resize(img):
    dim = (2000, 2000)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def generateText(path):
    image = Image.open(path)
    exifdata = image._getexif()

    make = exifdata.get(271)
    model = exifdata.get(272)
    focalLegth = exifdata.get(37386)
    shutterSpeed = math.ceil(1/float(exifdata.get(0x829a)))
    F = int(exifdata.get(37378))
    ISO = exifdata.get(34855)
    text = f"{make} {model} | {focalLegth} mm | f/{F} | SS 1/{shutterSpeed} | ISO {ISO}"
    return text

def printTextToImage(img, path, bottomBorder):
    text = generateText(path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if img.shape[1] >= img.shape[0]:
        squareSize = round(img.shape[1]+1000, -3)
    else:
        squareSize = round(img.shape[0]+1000, -3)
    fontsize = int(squareSize/1000 - 4)
    linewidth = fontsize + 5
    textsize = cv2.getTextSize(text, font, fontsize, linewidth )[0]
    color = (0, 0, 0)

    textX = int((img.shape[1] - textsize[0]) / 2)
    textY = bottomBorder + textsize[1] + 30  #int((img.shape[0] + textsize[1]) / 2)
    imageWithText = cv2.putText(img, text, ( textX, textY ), font, fontsize, color, linewidth)

    return imageWithText

directory = "Exports"
for Photo in os.listdir(directory):
    path = os.path.join(directory, Photo)
    image = cv2.imread(path)

    border, bottomBorder = addBorder(image)
    withText = printTextToImage(border, path, bottomBorder)
    cv2.imwrite(f"Processed/{Photo}", withText)
