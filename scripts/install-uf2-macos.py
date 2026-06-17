#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def notify(message: str, *, title: str = "TOTEM firmware") -> None:
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def find_one_firmware(firmware_dir: Path, pattern: str) -> Path:
    matches = sorted(path for path in firmware_dir.glob(pattern) if path.is_file())
    if len(matches) != 1:
        found = "\n".join(f"  {path}" for path in matches) or "  none"
        raise SystemExit(f"Expected exactly one firmware file matching {pattern!r} in {firmware_dir}; found:\n{found}")
    return matches[0]


def snapshot_volumes() -> dict[str, Path]:
    root = Path("/Volumes")
    if not root.exists():
        raise SystemExit("/Volumes does not exist. This installer is for macOS.")

    volumes: dict[str, Path] = {}
    for path in root.iterdir():
        if path.name.startswith("."):
            continue
        if path.is_dir() and os.access(path, os.W_OK):
            volumes[path.name] = path
    return volumes


def choose_volume(candidates: list[Path]) -> Path:
    if len(candidates) == 1:
        return candidates[0]

    print("\nMultiple new writable volumes appeared:")
    for idx, path in enumerate(candidates, start=1):
        print(f"  {idx}. {path}")

    while True:
        choice = input("Select the keyboard bootloader volume number: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(candidates):
                return candidates[index - 1]
        print("Invalid selection.")


def wait_for_new_volume(label: str, timeout_seconds: int) -> Path:
    baseline = snapshot_volumes()
    print(f"\n{label}: connect this half, then double-click reset to enter the UF2 bootloader.")
    print("Waiting for a new writable volume to appear in /Volumes ...")
    notify(f"Connect {label.lower()} half and double-click reset.")

    start = time.monotonic()
    while True:
        current = snapshot_volumes()
        new_names = sorted(set(current) - set(baseline))
        candidates = [current[name] for name in new_names]

        if candidates:
            volume = choose_volume(candidates)
            print(f"Detected bootloader volume: {volume}")
            return volume

        if timeout_seconds and time.monotonic() - start > timeout_seconds:
            raise SystemExit(f"Timed out waiting for {label} bootloader volume.")

        time.sleep(1)


def wait_for_disappear(volume: Path, timeout_seconds: int = 45) -> None:
    start = time.monotonic()
    while volume.exists() and time.monotonic() - start <= timeout_seconds:
        time.sleep(1)


def flash_half(label: str, firmware: Path, timeout_seconds: int, dry_run: bool) -> None:
    volume = wait_for_new_volume(label, timeout_seconds)
    destination = volume / firmware.name

    print(f"Installing {firmware.name} to {volume} ...")
    if dry_run:
        print(f"Dry run: would copy {firmware} -> {destination}")
        return

    shutil.copyfile(firmware, destination)
    os.sync()
    time.sleep(2)

    if volume.exists():
        subprocess.run(["diskutil", "eject", str(volume)], check=False)

    wait_for_disappear(volume)
    print(f"{label} firmware install step complete.")
    notify(f"{label} firmware install step complete.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install TOTEM UF2 firmware files on macOS, left half first.")
    parser.add_argument("--firmware-dir", type=Path, default=Path(__file__).resolve().parents[1] / "firmware")
    parser.add_argument("--left-pattern", default="*left*.uf2")
    parser.add_argument("--right-pattern", default="*right*.uf2")
    parser.add_argument("--timeout", type=int, default=0, help="Seconds to wait for each half; 0 waits forever.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight", action="store_true", help="Validate firmware file selection and exit.")
    args = parser.parse_args()

    if sys.platform != "darwin":
        raise SystemExit("This installer is for macOS because it watches /Volumes and uses diskutil.")

    firmware_dir = args.firmware_dir.expanduser().resolve()
    left = find_one_firmware(firmware_dir, args.left_pattern)
    right = find_one_firmware(firmware_dir, args.right_pattern)

    print("Firmware files:")
    print(f"  left:  {left}")
    print(f"  right: {right}")
    print("\nOrder: left half first, then right half.")

    if args.preflight:
        return 0

    flash_half("Left half", left, args.timeout, args.dry_run)
    print("\nDisconnect the left half. Connect the right half when ready.")
    flash_half("Right half", right, args.timeout, args.dry_run)

    print("\nBoth keyboard halves are installed.")
    notify("Both keyboard halves are installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
