from io import BytesIO
import string
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


class SimpleUploadedImage(SimpleUploadedFile):

    def __init__(self, name: str, height=64, width=64, color: tuple = None,
                 image_mime_type='jpeg'):

        color = color or (255, 255, 255)

        image_data = BytesIO()
        self.image = Image.new('RGB', (height, width), color)
        self.image.save(image_data, image_mime_type)

        content = image_data.getvalue()
        content_type = f'image/{image_mime_type}'

        super().__init__(name, content, content_type=content_type)


def strong_password(length):
    symbols = [
        *string.ascii_lowercase,
        *string.ascii_uppercase,
        *string.digits,
        *string.punctuation,
    ]

    random_set = random.sample(symbols, length)
    password = ''.join(random_set)

    return password
