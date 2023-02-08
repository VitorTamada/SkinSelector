import io
import os
import PIL.PngImagePlugin

from PIL import Image, ImageTk
from urllib.request import urlopen

NOT_SAVE = 'NO SAVE'
SAVE = 'SAVE'


class ImageManager:
    def __init__(self):
        self.__mode = SAVE
        self.__project_absolute_path = os.path.abspath('./')

    @property
    def current_mode(self):
        return self.__mode

    @property
    def project_absolute_path(self):
        return self.__project_absolute_path

    @staticmethod
    def _load_image_from_disk(relative_path):
        path = relative_path
        image = Image.open(path)
        photo_image = ImageTk.PhotoImage(image)

        return photo_image, image

    @staticmethod
    def resize_image(image, **kwargs):
        assert (isinstance(image, PIL.PngImagePlugin.PngImageFile) or isinstance(image,
                                                                                 PIL.JpegImagePlugin.JpegImageFile))
        if 'ratio' in kwargs:
            ratio = kwargs['ratio']
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            resized_image = image.resize(new_size)
            return ImageTk.PhotoImage(resized_image)
        elif 'new_size' in kwargs:
            new_size = kwargs['new_size']
            resized_image = image.resize(new_size)
            return ImageTk.PhotoImage(resized_image)

    def switch_mode(self):
        if self.__mode == NOT_SAVE:
            self.__mode = SAVE
        else:
            self.__mode = NOT_SAVE

    def _get_directory_to_save(self, path):
        if 'champion' in path:
            directory_path = path.split("/")[-3:]
        else:
            directory_path = path.split("/")[-1:]
        path_to_save = self.__project_absolute_path + "\\res\\" + "\\".join(directory_path)

        return path_to_save

    def _load_image_from_web(self, img_url):
        fin = urlopen(img_url)
        s = io.BytesIO(fin.read())
        image = Image.open(s)
        photo_image = ImageTk.PhotoImage(image)

        if self.__mode == SAVE:
            path_to_save = self._get_directory_to_save(img_url)
            image.save(path_to_save)

        return photo_image, image

    @staticmethod
    def _load_image_from_bytes(byte_string):
        return Image.open(io.BytesIO(byte_string))

    def load_image(self, path, is_chroma=None):
        if is_chroma:
            image_path = self._get_directory_to_save(path)
            if os.path.exists(image_path):
                return self._load_image_from_disk(image_path)
            else:
                chroma = self._load_image_from_bytes(is_chroma)
                pil_chroma = ImageTk.PhotoImage(chroma)
                if self.__mode == SAVE:
                    chroma.save(image_path)
                return pil_chroma, chroma
        else:
            if not os.path.exists(self._get_directory_to_save(path)):
                return self._load_image_from_web(path)
            else:
                image_path = self._get_directory_to_save(path)
                return self._load_image_from_disk(image_path)
