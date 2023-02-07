import io
import os

import PIL.PngImagePlugin

from PIL import Image, ImageTk
from urllib.request import urlopen


project_absolute_path = os.path.abspath("./")


def get_path_to_save(img_url):
    path = img_url.split("/")[-3:]
    path_to_save = project_absolute_path + "\\res"
    for elem in path:
        path_to_save += "\\" + elem

    return path_to_save


def load_image_from_web(img_url):
    fin = urlopen(img_url)
    s = io.BytesIO(fin.read())
    image = Image.open(s)
    path_to_save = get_path_to_save(img_url)
    image.save(path_to_save)
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


def load_image_from_bytes(byte_string):
    return Image.open(io.BytesIO(byte_string))


def load_image_from_disk(relative_path):
    path = os.getcwd() + relative_path
    image = Image.open(path)
    photo_image = ImageTk.PhotoImage(image)

    return photo_image, image


def load_image(image_path):
    if image_path.startswith("http://") and not os.path.exists(get_path_to_save(image_path)):
        return load_image_from_web(image_path)
    else:
        path = project_absolute_path + get_path_to_save(image_path)
        return load_image_from_disk(image_path)