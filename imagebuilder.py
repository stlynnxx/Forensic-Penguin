from pathlib import Path
import hashlib

from pathlib import Path
import hashlib

class ImageBuilder:
    def __init__(self):
        self.source = None
        self.destination = None
    def acquire(self):
        sha256 = hashlib.sha256()

        with self.source.open("rb") as src:
            with self.destination.open("xb") as dst:
                while True:
                    chunk = src.read(16)
                    print(f"Read {len(chunk)} bytes")

                    if not chunk:
                        break

                    dst.write(chunk)
                    sha256.update(chunk)

        return sha256.hexdigest()