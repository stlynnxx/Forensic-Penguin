from pathlib import Path


class BinaryReader:
    def __init__(self, image_path: Path):
        self.image_path = image_path
        self.image = None

    def open(self):
        self.image = self.image_path.open("rb")

    def read(self, offset: int, read_size: int) -> bytes:
        self.image.seek(offset)
        return self.image.read(read_size)

    def close(self):
        if self.image is not None:
            self.image.close()
            self.image = None