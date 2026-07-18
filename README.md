# MWFK - Microsoft Windows Key Finder

A CLI tool to look up **KMS client setup keys** for Windows and Office versions. (Made on a chromebook btw)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Cross--platform-green)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

## Features

- **59 KMS keys** across **13 product families**
- Windows XP through Windows 11, Server 2008 R2 through 2022, Office LTSC
- Color-coded terminal UI
- Auto-copy keys to clipboard (xclip/xsel/wl-copy/pbcopy)
- Flashing credit animation
- Centered ASCII art banner

## Installation

Clone the repository:

```bash
git clone https://github.com/PalmtreeDev-real/MWFK.git
cd MWFK
```

## Usage

```bash
./mwfk          # using the shell wrapper
python3 mwfk.py # or run directly
```

## Supported Products

| Family | Keys |
|--------|------|
| Windows 10/11 | 17 |
| Windows 8.1 | 4 |
| Windows 8 | 4 |
| Windows 7 | 5 |
| Windows Server 2022 | 2 |
| Windows Server 2019 | 3 |
| Windows Server 2016 | 3 |
| Windows Server 2012 R2 | 3 |
| Windows Server 2012 | 3 |
| Windows Server 2008 R2 | 5 |
| Windows Vista | 4 |
| Windows XP | 2 |
| Microsoft Office LTSC | 4 |

## Screenshot

```
                                                 
▄▄▄      ▄▄▄ ▄▄▄▄  ▄▄▄  ▄▄▄▄ ▄▄▄   ▄▄▄  ▄▄▄▄▄▄▄ 
████▄  ▄████ ▀███  ███  ███▀ ███ ▄███▀ ███▀▀▀▀▀ 
███▀████▀███  ███  ███  ███  ███████   ███▄▄    
███  ▀▀  ███  ███▄▄███▄▄███  ███▀███▄  ███▀▀    
███      ███   ▀████▀████▀   ███  ▀███ ███

          Microsoft Windows Key Finder  v1.0.0
          KMS Client Setup Key Reference

═══════════════════════════════════════════════════════
║               SELECT A PRODUCT FAMILY                ║
═══════════════════════════════════════════════════════

   1 │ Windows 10/11                 (17 keys)
   2 │ Windows 8.1                   (4 keys)
   3 │ Windows 8                     (4 keys)
   ...
   0 │ Exit
```

## Note

These are **KMS client setup keys** (also known as Generic Volume License Keys or GVLKs). They are publicly documented by Microsoft and are used for KMS client activation in enterprise environments. These are **not** retail or OEM product keys.

## Credits

Made by [PalmtreeDev-real](https://github.com/PalmtreeDev-real) on GitHub / atlasdevmc on Discord

## License

Licensed under the [Apache License 2.0](LICENSE).
