import io

import PIL.PngImagePlugin

from PIL import Image, ImageTk
from urllib.request import urlopen


def load_image_from_web(img_url):
    fin = urlopen(img_url)
    s = io.BytesIO(fin.read())
    image = Image.open(s)
    photo_image = ImageTk.PhotoImage(image)

    return photo_image, image


def resize_image_from_web(image, **kwargs):
    assert (isinstance(image, PIL.PngImagePlugin.PngImageFile) or isinstance(image, PIL.JpegImagePlugin.JpegImageFile))
    if 'ratio' in kwargs:
        ratio = kwargs['ratio']
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        resized_image = image.resize(new_size)
        return ImageTk.PhotoImage(resized_image)
    elif 'new_size' in kwargs:
        new_size = kwargs['new_size']
        resized_image = image.resize(new_size)
        return ImageTk.PhotoImage(resized_image)
