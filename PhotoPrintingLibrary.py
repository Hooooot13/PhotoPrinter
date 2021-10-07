import cv2
from PIL import Image
from PIL.ExifTags import TAGS
import math
import os

class photo:
    def __init__(self, path, title=""):
        #Read in image
        self.fileName = path.split('/')[-1]
        self.image = cv2.imread(path)
        self.title = title

        #Read EXIF Data
        imageEXIF = Image.open(path)
        self.exifdata = imageEXIF._getexif()

        self.make = self.exifdata.get(271)
        self.model = self.exifdata.get(272)
        self.focalLegth = self.exifdata.get(37386)
        self.shutterSpeed = float(self.exifdata.get(0x829a))

        if self.shutterSpeed >= 1.0:
            self.shutterSpeed = self.exifdata.get(0x829a)
            SSprint = f"{int(self.exifdata.get(0x829a))}"
        else:
            self.shutterSpeed = math.ceil(1/float(self.exifdata.get(0x829a)))
            SSprint = f"1/{self.shutterSpeed}"

        self.F = f"F/{round(float(self.exifdata.get(37378)), 1)}"
        self.ISO = self.exifdata.get(34855)

        #Generate text
        self.text = f"{self.make} {self.model} | {self.focalLegth} mm | {self.F} | SS {SSprint} | ISO {self.ISO}"

        #Calcualte Border
        if self.image.shape[1] >= self.image.shape[0]:
            self.squareSize = round(self.image.shape[1]+1000, -3)
        else:
            self.squareSize = round(self.image.shape[0]+1000, -3)
        self.top = int((self.squareSize-self.image.shape[0])/2)
        self.bottom = int((self.squareSize-self.image.shape[0])/2)
        self.left = int((self.squareSize-self.image.shape[1])/2)
        self.right = int((self.squareSize-self.image.shape[1])/2)
        self.ImageBottom = self.top + self.image.shape[0]

        #define border color (Default)
        self.borderColor = [255, 255, 255]

        #define the print size
        # These are all defaults
        self.printSize = [3, 3]
        self.dpi = 300
        self.finalResolution = (self.printSize[0]*self.dpi, self.printSize[1]*self.dpi)

        self.image_with_border = cv2.copyMakeBorder(self.image, self.top, self.bottom, self.left, self.right, cv2.BORDER_CONSTANT, value=self.borderColor)
        
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontsize = 4
        self.linewidth = 8
        self.textsize = cv2.getTextSize(self.text, self.font, self.fontsize, self.linewidth )[0]
        self.textColor = (0, 0, 0)

        textX = int((self.image_with_border.shape[1] - self.textsize[0]) / 2)
        textY = self.ImageBottom + self.textsize[1] + 30  #int((img.shape[0] + textsize[1]) / 2)
        self.imageWithText = cv2.putText(self.image_with_border, self.text, ( textX, textY ), self.font, self.fontsize, self.textColor, self.linewidth)

        self.titlesize = cv2.getTextSize(self.title, self.font, self.fontsize, self.linewidth )[0]
        textX = int((self.image_with_border.shape[1] - self.titlesize[0]) / 2)
        textY = self.top - self.titlesize[1] - 30
        self.imageWithText = cv2.putText(self.imageWithText, self.title, ( textX, textY ), self.font, self.fontsize, self.textColor, self.linewidth)

        self.resizedImage = cv2.resize(self.imageWithText, self.finalResolution, interpolation = cv2.INTER_AREA)
        

    def print(self):
        print('{0:24}: {1}'.format('Title', self.title))
        print('{0:24}: {1} {2}'.format('Camera', self.make, self.model))
        print('{0:24}: {1}'.format('Focal Length', self.focalLegth))
        print('{0:24}: {1}'.format('Shutter Speed', self.shutterSpeed))
        print('{0:24}: {1}'.format('Aperture', self.F))
        print('{0:24}: {1}'.format('ISO', self.ISO))
        print('{0:24}: {1}'.format('Image Text', self.text))
        print('Border Info')

    def show(self):
        cv2.imshow("Image Test",self.resizedImage)
        cv2.waitKey(0)
        #closing all open windows
        cv2.destroyAllWindows()

    def reProcess(self, newSize, fontsize, linewidth):
        self.squareSize = newSize
        self.top = int((self.squareSize-self.image.shape[0])/2)
        self.bottom = int((self.squareSize-self.image.shape[0])/2)
        self.left = int((self.squareSize-self.image.shape[1])/2)
        self.right = int((self.squareSize-self.image.shape[1])/2)
        self.ImageBottom = self.top + self.image.shape[0]

        self.image_with_border = cv2.copyMakeBorder(self.image, self.top, self.bottom, self.left, self.right, cv2.BORDER_CONSTANT, value=self.borderColor)

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontsize = fontsize
        self.linewidth = linewidth
        self.textsize = cv2.getTextSize(self.text, self.font, self.fontsize, self.linewidth )[0]
        self.textColor = (0, 0, 0)

        textX = int((self.image_with_border.shape[1] - self.textsize[0]) / 2)
        textY = self.ImageBottom + self.textsize[1] + 30  #int((img.shape[0] + textsize[1]) / 2)
        self.imageWithText = cv2.putText(self.image_with_border, self.text, ( textX, textY ), self.font, self.fontsize, self.textColor, self.linewidth)

        self.titlesize = cv2.getTextSize(self.title, self.font, self.fontsize, self.linewidth )[0]
        textX = int((self.image_with_border.shape[1] - self.titlesize[0]) / 2)
        textY = self.top - self.titlesize[1] - 30
        self.imageWithText = cv2.putText(self.imageWithText, self.title, ( textX, textY ), self.font, self.fontsize, self.textColor, self.linewidth)

        self.resizedImage = cv2.resize(self.imageWithText, self.finalResolution, interpolation = cv2.INTER_AREA)
    
    
    def save(self):
        cv2.imwrite(f"{self.fileName.split('.')[0]}_B.jpg", self.imageWithText)
