from PIL import Image
import pytesseract

img = Image.open('C:/Users/Abhay Singh/Desktop/image.png')
text = pytesseract.image_to_string(img)
print(text)