from pathlib import Path
import argparse
import binaryreader, imagebuilder
def main():
    parser = argparse.ArgumentParser(
        description="ForensicPenguin: A File Forensics Tool"
    )
    parser.add_argument(
        "-i", "--image",
        type=Path,
        help="Path to an existing disk image"
    )

    parser.add_argument(
        "-b", "--build",
        action="store_true",
        help="Acquire an image of the local machine"
    )
    parser.add_argument(
        "--offset", "-o", default=0, type=int, help="Offset from image"
    )
    parser.add_argument(
        "--read_size", "-r", default=64, type=int, help="Read size in bytes"
    )
    args = parser.parse_args()
    if args.build == (args.image is not None):
        parser.error("Specify either --build or --image")
    # Assigning the path with either in house build or supplied path
    if args.build:
        builder = imagebuilder.ImageBuilder()
        image_path = builder.acquire()
    else:
        image_path = args.image
    # Checking offset and readsizes
    if args.offset < 0:
        parser.error("Offset cannot be negative")
    if args.read_size <= 0:
        parser.error("Read size must be greater than zero")
    # Assigning offset and read sizes
    offset = args.offset
    read_size = args.read_size
    # checking image_path
    if not image_path.is_file():
        parser.error(f"Invalid image file: {image_path}")
    # Getting image size
    image_size = image_path.stat().st_size
    print(f"Image size: {image_size} bytes")
    reader = binaryreader.BinaryReader(image_path)
    try:
        reader.open()
        data = reader.read(offset, read_size)
        print(f"Read results: {data.hex(' ')}")

    finally:
        reader.close()

if __name__ == "__main__":
    main()