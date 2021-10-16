from PhotoPrintingLibrary import photo
from PhotoPrintingLibrary import collage
import os


#A Boy and His Camera (vertical)
Photo1 = photo(f"Exports\PXL_20210922_044429634.jpg", "A Boy and His Camera")
#Photo1.reProcess(3000, 0.5, 1)
Photo1.save()

#Power Lines (Vertical)
Photo2 = photo(f"Exports\IMG_0482.jpg", "Power Lines")
Photo2.save()

#Byodo-In Temple (Horizontal)
Photo3 = photo(f"Exports\DSCF0691-Edit.jpg", "Byodo-In Temple")
Photo3.save()

#Nap Time (Horizontal)
Photo4 = photo(f"Exports\DSCF1193.jpg", "Nap Time")
Photo4.save()

#I like This Guy (Horizontal)
Photo5 = photo(f"Exports\DSCF2067.jpg", "I like This Guy")
Photo5.save()

#The Corridor (Verticle)
Photo6 = photo(f"Exports\DSCF8855.jpg", "The Corridor")
Photo6.save()

#Elk Breakfast (Horizontal)
Photo7 = photo(f"Exports\DSCF0987.jpg", "Elk Breakfast")
Photo7.save()

#Jurassic Park (Horizontal)
Photo8 = photo(f"Exports\DSCF0803.jpg", "Jurassic Park")
Photo8.save()

#The Spider (Horizontal)
Photo9 = photo(f"Exports\DSCF0063.jpg", "The Spider")
Photo9.save()

collage([Photo9.imageWithText, Photo5.imageWithText, Photo8.imageWithText, +
        Photo6.imageWithText, Photo1.imageWithText, Photo2.imageWithText, +
        Photo4.imageWithText, Photo3.imageWithText, Photo7.imageWithText])