# Forensic-Penguin

Forensic-Penguin is a Python-based digital forensics and disk acquisition tool for Linux designed to simplify the process of acquiring and examining digital evidence.
The goal is to provide a self-contained forensic utility capable of identifying local storage devices, creating forensic disk images, and performing binary-level analysis without requiring users to rely on separate imaging software.
Development Status: Beta — Active Development
Forensic-Penguin is being developed with an emphasis on straightforward operation, modularity, and evidence integrity.
Development Status: Beta — Active Development

**Features**
----------
Disk Image Acquisition
Forensic-Penguin's acquisition engine, ImageBuilder, is being developed to support imaging storage devices directly from the machine running the application.

Current development includes:
Linux block-device discovery using lsblk.
Identification of local storage devices and mounted filesystems.
Source and destination validation.
Raw, chunk-based data acquisition.
SHA-256 hashing during acquisition.
Integration between image acquisition and binary analysis.
Automatic system-disk acquisition, destination safety checks, and completed-image verification are areas of ongoing development and testing.
Binary Image Analysis

Forensic-Penguin includes a BinaryReader component for examining existing disk images.

Current functionality includes:
Opening disk images in read-only binary mode.
Reading data at specified byte offsets.
Configurable read sizes.
Displaying extracted bytes in hexadecimal format.
Basic input validation and file handling.
Modular Architecture



**Usage**
------
Analyze an Existing Image
Use -i or --image to specify an existing disk image.
```bash
python forensicpenguin.py -i evidence.img
```

Read 128 bytes beginning at offset 512:
```bash
python forensicpenguin.py -i evidence.img -o 512 -r 128
```

Build an Image

The -b or --build option is intended to initiate local disk acquisition through ImageBuilder.
```bash
python forensicpenguin.py -b
```

Note: Automatic live-system acquisition remains under development. Availability and behavior depend on the current beta implementation. Do not assume that all storage configurations are supported.



**Forensic Integrity and Limitations**
--------
Forensic-Penguin is an experimental forensic utility and should not currently be treated as a validated forensic acquisition solution.
Important considerations include:
Live acquisition: Filesystems on running machines may change during acquisition, potentially producing inconsistent images.
Evidence integrity: SHA-256 hashing supports integrity checking but does not independently establish the forensic soundness of an acquisition.
Storage configurations: Encrypted volumes, RAID, LVM, and other complex configurations may not be fully supported.
Device permissions: Physical storage access may require administrative privileges.

Evidence preservation: Operators are responsible for selecting safe destinations and maintaining appropriate evidence-handling procedures.

Forensic-Penguin should be tested against disposable data and noncritical systems before use in sensitive environments.

**Contributing**
--------
Contributions, bug reports, testing, and constructive feedback are welcome.

ForensicPenguin is under active development, and its architecture and functionality may change between beta releases.

Before submitting a pull request:
Review existing issues and discussions.
Keep changes focused on the issue or functionality being addressed.
Explain the purpose of your changes.
Test changes where practical.
Avoid unrelated modifications.
Contributions involving acquisition or evidence handling should prioritize data safety, predictable behavior, and clear reporting of failures.

**Disclaimer**
--------
ForensicPenguin is provided for educational, research, and authorized digital forensic purposes.
The software is currently in beta development and is provided without guarantees of forensic accuracy, evidence admissibility, or suitability for professional investigations.
Users are responsible for obtaining appropriate authorization before examining or acquiring data from any system.
Never perform untested acquisition operations against critical storage devices.
