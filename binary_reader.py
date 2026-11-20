import os


def read(image_path, offset, read_size):
    with image_path.open("rb") as image:
        image.seek(offset)
        return image.read(read_size)
