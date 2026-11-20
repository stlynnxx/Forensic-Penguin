from pathlib import Path
import argparse
import binary_reader

def main():
    data_import = {}
    read_size = 64
    offset = 0
    parser = argparse.ArgumentParser(
        description="ForensicPenguin: A File Forensics Tool"
    )

    parser.add_argument(
        "-i",
        "--image",
        required=True,
        type=Path,
        help="Path to the disk image"
    )
    parser.add_argument(
        "--offset", "-o", default=0, type=int, help="Offset from image"
    )
    parser.add_argument(
        "--read_size", "-r", default=64, type=int, help="Read size in bytes"
    )
    args = parser.parse_args()
    image_path = args.image
    if args.offset < 0:
        parser.error("Offset cannot be negative")

    if args.read_size <= 0:
        parser.error("Read size must be greater than zero")

    offset = args.offset
    read_size = args.read_size

    if not image_path.is_file():
        parser.error(f"Invalid image file: {image_path}")
    image_size = image_path.stat().st_size
    print(f"Image size: {image_size} bytes")
    data = binary_reader.read(image_path, offset, read_size)
    print(f"Read results: {data.hex(' ')}")


if __name__ == "__main__":
    main()