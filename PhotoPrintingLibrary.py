import cv2
from PIL import Image
from PIL.ExifTags import TAGS
import math
import numpy as np
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
            self.squareSize = self.image.shape[1]+int(self.image.shape[1]/12)
        else:
            self.squareSize = self.image.shape[0]+int(self.image.shape[0]/12)
        self.top = int((self.squareSize-self.image.shape[0])/2)
        self.bottom = int((self.squareSize-self.image.shape[0])/2)
        self.left = int((self.squareSize-self.image.shape[1])/2)
        self.right = int((self.squareSize-self.image.shape[1])/2)
        self.ImageBottom = self.top + self.image.shape[0]

        #define border color (Default)
        self.borderColor = [255, 255, 255]

        #define the print size
        # These are all defaults
        self.printSize = [12, 12]
        self.dpi = 300
        self.finalResolution = (3600, 3600)

        self.image_with_border = cv2.copyMakeBorder(self.image, self.top, self.bottom, self.left, self.right, cv2.BORDER_CONSTANT, value=self.borderColor)
        
        self.resizedImage = cv2.resize(self.image_with_border, self.finalResolution, interpolation = cv2.INTER_AREA)
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontsize = 1#*(self.squareSize/2000)
        self.linewidth = 2#int(1*(self.squareSize/2000))
        self.textsize = cv2.getTextSize(self.text, self.font, self.fontsize, self.linewidth )[0]
        self.textColor = (0, 0, 0)

        textX = int((self.resizedImage.shape[1]- self.textsize[0]) / 2)
        textY = int((self.ImageBottom*(3600/self.squareSize))  + self.textsize[1]*2)  #int((img.shape[0] + textsize[1]) / 2)
        self.imageWithText = cv2.putText(self.resizedImage, self.text, ( textX, textY ), self.font, self.fontsize, self.textColor, self.linewidth)

        self.titlesize = cv2.getTextSize(self.title, self.font, self.fontsize, self.linewidth )[0]
        textX = int(((self.resizedImage.shape[1]  - self.titlesize[0]) / 2))
        textY = int((self.top*(3600/self.squareSize))  - (self.titlesize[1]))
        self.imageWithText = cv2.putText(self.resizedImage, self.title, ( textX, textY ), self.font, self.fontsize, self.textColor, self.linewidth)

        

        print(f"{self.title} {self.squareSize}")
        

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


def collage(arrayIM):
    spacing = 300
    
    for i in range(len(arrayIM)):
        #arrayIM[i] = cv2.resize(arrayIM[i], (2000, 2000), interpolation = cv2.INTER_AREA)
        arrayIM[i] = cv2.copyMakeBorder(arrayIM[i], 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        arrayIM[i] = cv2.copyMakeBorder(arrayIM[i], spacing, spacing, spacing, spacing, cv2.BORDER_CONSTANT, value=(246, 249, 250))
    
    H1 = np.hstack([arrayIM[0], arrayIM[1], arrayIM[2]])
    H2 = np.hstack([arrayIM[3], arrayIM[4], arrayIM[5]])
    H3 = np.hstack([arrayIM[6], arrayIM[7], arrayIM[8]])

    V = np.vstack([H1, H2, H3])

    cv2.imwrite("Arangment.jpg", V)