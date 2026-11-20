from pathlib import Path
import argparse

def main():
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

    args = parser.parse_args()
    image_path = args.image
    image_size = image_path.stat().st_size
    if not image_path.is_file():
        parser.error(f"Invalid image file: {image_path}")
    print(f"Image size: {image_size} bytes")

