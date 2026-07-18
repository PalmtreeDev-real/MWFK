#!/usr/bin/env python3
"""
MWFK - Microsoft Windows Key Finder
A CLI tool to look up KMS client setup keys for Windows versions.
"""

import os
import sys
import shutil
import subprocess
import time

VERSION = "1.0.0"

# ─── KMS Key Database ────────────────────────────────────────────────────────

KMS_KEYS = {
    "Windows 10/11": [
        {"edition": "Windows 10/11 Pro",                       "key": "W269N-WFGWX-YVC9B-4J6C9-T83GX"},
        {"edition": "Windows 10/11 Pro N",                     "key": "MH37W-N47XK-V7XM9-C7227-GCQG9"},
        {"edition": "Windows 10/11 Pro for Workstations",      "key": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"},
        {"edition": "Windows 10/11 Pro for Workstations N",    "key": "9FNHH-K3HBT-3W4TD-6383H-6XYWF"},
        {"edition": "Windows 10/11 Pro Education",             "key": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y"},
        {"edition": "Windows 10/11 Pro Education N",           "key": "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC"},
        {"edition": "Windows 10/11 Education",                 "key": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2"},
        {"edition": "Windows 10/11 Education N",               "key": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"},
        {"edition": "Windows 10/11 Enterprise",                "key": "NPPR9-FWDCX-D2C8J-H872K-2YT43"},
        {"edition": "Windows 10/11 Enterprise N",              "key": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4"},
        {"edition": "Windows 10/11 Enterprise G",              "key": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B"},
        {"edition": "Windows 10/11 Enterprise G-N",            "key": "44RPN-FTY23-9VTTB-MP9BX-T84FV"},
        {"edition": "Windows 10/11 Enterprise LTSC 2021",     "key": "M7XTQ-FN8P6-TTKYV-9D2CC-R44DR"},
        {"edition": "Windows 10/11 Enterprise LTSC 2021 N",   "key": "C6H6D-7W6W3-7JR78-M6HWJ-X493G"},
        {"edition": "Windows 10/11 IoT Enterprise",           "key": "XTCBR-FYGVR-YKG9W-MPJDP-3H3YF"},
        {"edition": "Windows 10/11 IoT Enterprise LTSC 2021", "key": "M7XTQ-FN8P6-TTKYV-9D2CC-R44DR"},
        {"edition": "Windows 10/11 SE",                        "key": "KY7PN-VR6TX-3Q6XY-PMQXM-7XQ4G"},
    ],
    "Windows 8.1": [
        {"edition": "Windows 8.1 Pro",                         "key": "GCRJD-8NW9H-F2CDX-CCM8D-9D6T9"},
        {"edition": "Windows 8.1 Pro N",                       "key": "HMCNV-VVBFX-7HMBH-CTY9B-B4FXY"},
        {"edition": "Windows 8.1 Enterprise",                  "key": "MHF9N-XY6XB-VVXM4-C7CTX-H743Y"},
        {"edition": "Windows 8.1 Enterprise N",                "key": "TT4HM-HN7YT-62K67-RGRQJ-JFFXW"},
    ],
    "Windows 8": [
        {"edition": "Windows 8 Pro",                           "key": "NG4HW-VH26C-733KW-K6F98-J8CK4"},
        {"edition": "Windows 8 Pro N",                         "key": "XCVCF-2NXM9-723CB-MPBMB-YPK2V"},
        {"edition": "Windows 8 Enterprise",                    "key": "32JNW-9KQ84-P47T8-D8GGY-CWCK7"},
        {"edition": "Windows 8 Enterprise N",                  "key": "JMNMF-RHW7P-DMY6X-RF3DR-X2BQG"},
    ],
    "Windows 7": [
        {"edition": "Windows 7 Professional",                  "key": "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4"},
        {"edition": "Windows 7 Professional N",                "key": "MRPKT-YTG23-K7D7X-TWYHC-2H99G"},
        {"edition": "Windows 7 Enterprise",                    "key": "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH"},
        {"edition": "Windows 7 Enterprise N",                  "key": "YDRBP-3DYP3-CTTX6-XTYC6-2F99V"},
        {"edition": "Windows 7 Embedded POSReady",             "key": "YGMFT-WKD79-RMP8V-6C9FT-766DR"},
    ],
    "Windows Server 2022": [
        {"edition": "Windows Server 2022 Datacenter",         "key": "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"},
        {"edition": "Windows Server 2022 Standard",            "key": "VDYBN-27WPP-V4HQT-9VMD4-VMK7H"},
    ],
    "Windows Server 2019": [
        {"edition": "Windows Server 2019 Datacenter",         "key": "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"},
        {"edition": "Windows Server 2019 Standard",            "key": "N69G4-B89J2-4G8F4-WWYCC-J464C"},
        {"edition": "Windows Server 2019 Essentials",          "key": "WVDHN-86M7X-466P6-VHXV7-YY726"},
    ],
    "Windows Server 2016": [
        {"edition": "Windows Server 2016 Datacenter",         "key": "CB7KF-BWN84-R7R2Y-GR943-BR889"},
        {"edition": "Windows Server 2016 Standard",            "key": "WC2BQ-8NRM3-FDDYY-2BFGV-KHKQY"},
        {"edition": "Windows Server 2016 Essentials",          "key": "JCKRF-N37P4-C2D82-9YXRT-4M63B"},
    ],
    "Windows Server 2012 R2": [
        {"edition": "Windows Server 2012 R2 Datacenter",      "key": "W3GGN-FT8W3-Y4M27-J84CP-Q3VJ9"},
        {"edition": "Windows Server 2012 R2 Standard",         "key": "D2N9P-3P6X9-2R32C-3BP62-6967T"},
        {"edition": "Windows Server 2012 R2 Essentials",       "key": "KNCX8-JDV6C-HMQ6J-7H3X8-RQRCB"},
    ],
    "Windows Server 2012": [
        {"edition": "Windows Server 2012 Datacenter",         "key": "48HP8-DN98B-MYWDG-T2DCC-8W83P"},
        {"edition": "Windows Server 2012 Standard",            "key": "XC9B7-NBPP2-83J2H-RHMBY-92BT4"},
        {"edition": "Windows Server 2012 Essentials",          "key": "HM7DN-6H43T-KH499-4YGQW-GR8FT"},
    ],
    "Windows Server 2008 R2": [
        {"edition": "Windows Server 2008 R2 Datacenter",      "key": "74YFP-3QFB3-KQT8W-PMXWJ-7M648"},
        {"edition": "Windows Server 2008 R2 Standard",         "key": "YC6KT-GKW9T-YTKYR-T4X34-R7VHC"},
        {"edition": "Windows Server 2008 R2 Enterprise",       "key": "489J6-VHDMP-X63PK-3K798-CPX3Y"},
        {"edition": "Windows Server 2008 R2 HPC",              "key": "RCTBG-XCR7J-RV974-M7HRJ-WYFCR"},
        {"edition": "Windows Server 2008 R2 Web",              "key": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y"},
    ],
    "Windows Vista": [
        {"edition": "Windows Vista Business",                  "key": "YFKBB-TQ624-CPQVM-YYQVV-HX3K2"},
        {"edition": "Windows Vista Business N",                "key": "VX277-H3KD3-Y9WVP-WMDV6-H8779"},
        {"edition": "Windows Vista Enterprise",                "key": "VKK3Q-VC83F-HM3C9-T4724-YGT26"},
        {"edition": "Windows Vista Enterprise N",              "key": "VTC7F-BXVNM-YM836-BXMGT-FY3Y7"},
    ],
    "Windows XP": [
        {"edition": "Windows XP Professional",                 "key": "RMTHB-KRRVK-QY626-G7Y82-4YQ47"},
        {"edition": "Windows XP Professional N",               "key": "M7XQ9-8N2R8-7BJ6Y-3B4Y9-4G2T4"},
    ],
    "Microsoft Office LTSC 2024": [
        {"edition": "Office LTSC Professional Plus 2024",     "key": "XJ2YN-FMQ2C-JYXXP-4WGT7-MGQHV"},
        {"edition": "Office LTSC Standard 2024",               "key": "V28N4-JG22K-W66P8-VTMGK-H6HGR"},
        {"edition": "Office LTSC Professional Plus 2021",     "key": "FXYTK-NJJ8C-GB6DW-3DYQT-6F7TH"},
        {"edition": "Office LTSC Standard 2021",               "key": "KDX7X-BNVR8-TXXGX-4Q7Y8-78VT3"},
    ],
}

# ─── ANSI Codes ───────────────────────────────────────────────────────────────

BOLD    = "\033[1m"
DIM     = "\033[2m"
RESET   = "\033[0m"
CYAN    = "\033[36m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
RED     = "\033[31m"
MAGENTA = "\033[35m"
WHITE   = "\033[97m"
BG_DARK = "\033[48;5;236m"

ASCII_ART = f"""{CYAN}{BOLD}                                                 
▄▄▄      ▄▄▄ ▄▄▄▄  ▄▄▄  ▄▄▄▄ ▄▄▄   ▄▄▄  ▄▄▄▄▄▄▄ 
████▄  ▄████ ▀███  ███  ███▀ ███ ▄███▀ ███▀▀▀▀▀ 
███▀████▀███  ███  ███  ███  ███████   ███▄▄    
███  ▀▀  ███  ███▄▄███▄▄███  ███▀███▄  ███▀▀    
███      ███   ▀████▀████▀   ███  ▀███ ███{RESET}"""

SUBTITLE = f"{YELLOW}{BOLD}Microsoft Windows Key Finder{RESET}  {DIM}v{VERSION}{RESET}"
CREDIT   = "Made by Palmtreedev-real on github or atlasdevmc on discord"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_terminal_width():
    return shutil.get_terminal_size((80, 24)).columns

BLUE = "\033[34m"
LBLUE = "\033[94m"

def strip_ansi(text):
    import re
    return re.sub(r'\033\[[0-9;]*m', '', text)

def print_centered(text):
    w = get_terminal_width()
    plain = strip_ansi(text)
    pad = max(0, (w - len(plain)) // 2)
    print(" " * pad + text)

def print_banner():
    for line in ASCII_ART.splitlines():
        print_centered(line)
    print()
    print_centered(SUBTITLE)
    sub_plain = strip_ansi(SUBTITLE)
    w = get_terminal_width()
    pad = max(0, (w - len(sub_plain)) // 2)
    dim_line = f"{DIM}KMS Client Setup Key Reference{RESET}"
    print(" " * pad + dim_line)

def flash_credit():
    text = CREDIT
    w = get_terminal_width()
    plain_len = len(text)
    pad = max(0, (w - plain_len) // 2)
    padded = " " * pad + text
    padded_full = padded.ljust(w)
    for _ in range(6):
        sys.stdout.write(f"\r\033[2K{BLUE}{BOLD}{padded_full}{RESET}")
        sys.stdout.flush()
        time.sleep(0.15)
        sys.stdout.write(f"\r\033[2K{LBLUE}{BOLD}{padded_full}{RESET}")
        sys.stdout.flush()
        time.sleep(0.15)
    print(f"\r\033[2K{LBLUE}{BOLD}{padded_full}{RESET}")

def print_header(title):
    w = get_terminal_width()
    inner = w - 4
    print(f"{CYAN}{BOLD}╔{'═' * inner}╗{RESET}")
    print(f"{CYAN}{BOLD}║{RESET}{WHITE}{BOLD} {title.center(inner - 1)}{RESET}{CYAN}{BOLD}║{RESET}")
    print(f"{CYAN}{BOLD}╚{'═' * inner}╝{RESET}")

def print_separator():
    w = get_terminal_width()
    print(f"{DIM}{'─' * w}{RESET}")

def copy_to_clipboard(text):
    try:
        if shutil.which("xclip"):
            p = subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode(), capture_output=True
            )
            return p.returncode == 0
        elif shutil.which("xsel"):
            p = subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=text.encode(), capture_output=True
            )
            return p.returncode == 0
        elif shutil.which("wl-copy"):
            p = subprocess.run(
                ["wl-copy"], input=text.encode(), capture_output=True
            )
            return p.returncode == 0
        elif os.name == "nt":
            subprocess.run(
                ["clip"], input=text.encode(), capture_output=True
            )
            return True
        elif shutil.which("pbcopy"):
            p = subprocess.run(
                ["pbcopy"], input=text.encode(), capture_output=True
            )
            return p.returncode == 0
    except Exception:
        pass
    return False

def count_total_keys():
    return sum(len(v) for v in KMS_KEYS.values())

# ─── Core Logic ───────────────────────────────────────────────────────────────

def list_categories():
    print_header("SELECT A PRODUCT FAMILY")
    print()
    categories = list(KMS_KEYS.keys())
    for i, cat in enumerate(categories, 1):
        count = len(KMS_KEYS[cat])
        print(f"  {YELLOW}{BOLD}{i:>2}{RESET} │ {WHITE}{BOLD}{cat:<30s}{RESET} {DIM}({count} keys){RESET}")
    print()
    print(f"  {DIM}  0  │ Exit{RESET}")
    print()
    return categories

def show_keys(category, keys):
    print_header(category)
    print()
    print(f"  {DIM}{'#':>2} │ {'Edition':<40s} │ {'KMS Client Setup Key'}{RESET}")
    print(f"  {DIM}{'──':>2}─┼─{'─' * 40}─┼─{'─' * 36}{RESET}")
    for i, entry in enumerate(keys, 1):
        is_alt = i % 2 == 0
        bg = BG_DARK if is_alt else ""
        print(f"  {YELLOW}{BOLD}{i:>2}{RESET} │ {WHITE}{entry['edition']:<40s}{RESET} │ {GREEN}{BOLD}{entry['key']}{RESET}")
    print()
    print(f"  {DIM}Tip: Enter a number to view and copy a key{RESET}")
    print(f"  {DIM}     Enter 'all' to display all keys formatted{RESET}")
    print(f"  {DIM}     Enter 'b' to go back{RESET}")
    print()

def show_all_keys_formatted(category, keys):
    print()
    print(f"{CYAN}{BOLD}── {category} ──{RESET}")
    print()
    for i, entry in enumerate(keys, 1):
        print(f"  {WHITE}{entry['edition']}{RESET}")
        print(f"  {GREEN}{BOLD}{entry['key']}{RESET}")
        print()
    print_separator()

def main():
    clear()
    print_banner()
    flash_credit()
    print()
    total = count_total_keys()
    print(f"  {DIM}A reference tool for Microsoft KMS client setup keys.{RESET}")
    print(f"  {DIM}Database contains {total} keys across {len(KMS_KEYS)} product families.{RESET}")
    print(f"  {DIM}These are publicly documented Generic Volume License Keys{RESET}")
    print(f"  {DIM}published by Microsoft for KMS client activation.{RESET}")
    print()
    input(f"  {CYAN}{BOLD}Press Enter to continue...{RESET}")

    while True:
        clear()
        print_banner()
        flash_credit()
        print()
        categories = list_categories()
        try:
            choice = input(f"  {CYAN}{BOLD}❯ Select a product family [0-{len(categories)}]: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0" or choice.lower() in ("q", "quit", "exit"):
            clear()
            print(
                f"{CYAN}{BOLD}"
                "___________.__                   __           ._.\n"
                "\\__    ___/|  |__ _____    ____ |  | __  _____| |\n"
                "  |    |   |  |  \\__  \\  /    \\|  |/ / /  ___/ |\n"
                "  |    |   |   Y  \\/ __ \\|   |  \\    <  \\___ \\ \\|\n"
                "  |____|   |___|  (____  /___|  /__|_ \\/____  >__\n"
                "                \\/     \\/     \\/     \\/     \\/ \\/"
                f"{RESET}\n\n"
                f"  {YELLOW}{BOLD}Thanks for using MWFK!{RESET}\n\n"
                f"  {DIM}Made by Palmtreedev-real on github aka atlasdevmc on discord{RESET}\n"
            )
            input(f"  {DIM}Press Enter to exit...{RESET}")
            break

        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(categories):
                raise ValueError
        except ValueError:
            print(f"  {RED}Invalid choice. Try again.{RESET}")
            input(f"  {DIM}Press Enter...{RESET}")
            continue

        selected_category = categories[idx]
        selected_keys = KMS_KEYS[selected_category]

        while True:
            clear()
            show_keys(selected_category, selected_keys)
            flash_credit()

            try:
                sub = input(f"  {CYAN}{BOLD}❯ Pick a key [1-{len(selected_keys)}, 'all', 'b']: {RESET}").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return

            if sub.lower() in ("b", "back", ""):
                break

            if sub.lower() == "all":
                clear()
                show_all_keys_formatted(selected_category, selected_keys)
                print()
                input(f"  {DIM}Press Enter to go back...{RESET}")
                continue

            try:
                key_idx = int(sub) - 1
                if key_idx < 0 or key_idx >= len(selected_keys):
                    raise ValueError
            except ValueError:
                print(f"  {RED}Invalid choice. Try again.{RESET}")
                input(f"  {DIM}Press Enter...{RESET}")
                continue

            entry = selected_keys[key_idx]
            key = entry["key"]
            edition = entry["edition"]

            clear()
            print()
            print_header("KEY DETAILS")
            print()
            print(f"  {DIM}Edition:{RESET}  {WHITE}{BOLD}{edition}{RESET}")
            print(f"  {DIM}Key:{RESET}      {GREEN}{BOLD}{key}{RESET}")
            print()

            if copy_to_clipboard(key):
                print(f"  {GREEN}Copied to clipboard!{RESET}")
            else:
                print(f"  {YELLOW}Could not copy to clipboard (install xclip/xsel/wl-copy){RESET}")

            print()
            print(f"  {DIM}Press Enter to go back...{RESET}")
            input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {GREEN}{BOLD}Goodbye!{RESET}\n")
        sys.exit(0)
