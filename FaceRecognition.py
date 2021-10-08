from PIL import Image

#Load the image
img = Image.open('image.jfif')

#Get basic details about the image
print(img.format)
print(img.mode)
print(img.size)

#show the image
img.show()