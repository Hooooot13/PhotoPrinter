import cv2
from PIL import Image
from PIL.ExifTags import TAGS
import math
import os

class photo:
    def __init__(self, path, title):
        self.image = cv2.imread(path)
        self.title = title

        #Read EXIF Data
        image = Image.open(path)
        exifdata = image._getexif()

        self.make = exifdata.get(271)
        self.model = exifdata.get(272)
        self.focalLegth = exifdata.get(37386)
        self.shutterSpeed = math.ceil(1/float(exifdata.get(0x829a)))
        self.F = int(exifdata.get(37378))
        self.ISO = exifdata.get(34855)

        #Generate text
        self.text = f"{make} {model} | {focalLegth} mm | f/{F} | SS 1/{shutterSpeed} | ISO {ISO}"


    def print(self):
        print('{0:24} {1}'.format('Title', self.title))
