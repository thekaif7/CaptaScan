import cv2
import numpy as np
from captcha.image import ImageCaptcha
import pytesseract
from PIL import Image

# Update the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def generate_captcha():
    captcha_text = ''.join(np.random.choice(list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'), size=6))
    image = ImageCaptcha(width=150, height=60)
    captcha_image_bytesio = BytesIO(image.generate(captcha_text).getvalue())
    captcha_image_np = np.array(Image.open(captcha_image_bytesio).convert('RGB'))
    return captcha_text, captcha_image_np

def recognize_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(binary_image)
    return text

def main():
    captcha_text, captcha_image = generate_captcha()
    cv2.imshow('CAPTCHA', captcha_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    recognized_text = recognize_text_from_image(captcha_image)
    if recognized_text.lower() == captcha_text.lower():
        print("CAPTCHA verification successful!")
    else:
        print("CAPTCHA verification failed.")

if __name__ == "__main__":
    main()