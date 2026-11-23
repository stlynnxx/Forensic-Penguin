import json
import stat
import subprocess
from pathlib import Path
import hashlib


class ImageBuilder:
    def __init__(self):
        self.source = None
        self.destination = None
        self.sha256 = None

    def discover(self):
        result = subprocess.run(
            ["lsblk", "-J", "-o", "NAME,PATH,TYPE,SIZE,FSTYPE,MOUNTPOINTS"],
            capture_output=True,
            text=True,
            check=True
        )
        devices = json.loads(result.stdout)["blockdevices"]

        # Look for the physical disk containing the running root filesystem.
        # The hierarchy is not sufficient for every LVM/RAID/overlay setup.
        disks = [device for device in devices if device["type"] == "disk"]
        system_disks = [device for device in disks if self.contains_root(device)]

        if len(system_disks) != 1:
            raise RuntimeError(
                "Could not uniquely identify the system disk. "
                "Automatic acquisition is not supported for this storage layout yet."
            )

        self.source = Path(system_disks[0]["path"])
        return disks

    def contains_root(self, device):
        if "/" in (device.get("mountpoints") or []):
            return True

        for child in device.get("children", []):
            if self.contains_root(child):
                return True

        return False

    def validate_destination(self):
        if self.destination is None:
            raise ValueError("No destination selected")

        if self.destination.exists():
            raise FileExistsError(
                f"Destination already exists: {self.destination}"
            )

        if not self.destination.parent.is_dir():
            raise NotADirectoryError(
                f"Invalid destination directory: {self.destination.parent}"
            )

        # Resolve the destination filesystem to its backing block devices.
        # Refuse acquisition when this cannot be established safely.
        result = subprocess.run(
            ["findmnt", "-n", "-o", "SOURCE", "--target", str(self.destination.parent)],
            capture_output=True,
            text=True,
            check=True
        )
        mount_source = result.stdout.strip().split("[")[0]
        if not mount_source.startswith("/dev/"):
            raise RuntimeError(
                "Cannot verify destination storage. Use a separately mounted "
                "block-device evidence drive."
            )

        result = subprocess.run(
            ["lsblk", "-s", "-n", "-o", "PATH,TYPE", mount_source],
            capture_output=True,
            text=True,
            check=True
        )
        lines = [line.split() for line in result.stdout.splitlines() if line.strip()]
        backing_disks = {
            Path(parts[0]).resolve()
            for parts in lines
            if len(parts) == 2 and parts[1] == "disk"
        }
        if not backing_disks:
            raise RuntimeError("Could not establish destination's backing physical disk")
        if self.source.resolve() in backing_disks:
            raise RuntimeError("Destination is on the disk being acquired")

    def validate_source(self):
        if self.source is None:
            raise ValueError("No acquisition source selected")