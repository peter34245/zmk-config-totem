---
name: build
description: Project-local TOTEM ZMK workflow. Use when the user types /build, invokes $build, asks to build firmware after editing config/totem.keymap, asks to download GitHub Actions UF2 artifacts, or asks to install/flash the left and right TOTEM keyboard halves on macOS.
---

# TOTEM ZMK Build And Install

This is a repo-scoped skill for `/Users/ozz/Documents/GitHub/zmk-config-totem`.
Do not use or create global Codex skills for this workflow.

## Build Only

Run:

```bash
./scripts/build-firmware-github.sh "Update keymap"
```

This commits firmware source edits from `config`, `build.yaml`, and
`.github/workflows`, pushes the current branch, waits for GitHub Actions, and
downloads the two `.uf2` files into `firmware/`.

## Build And Install

Run:

```bash
./scripts/build-and-install.sh "Update keymap"
```

This builds through GitHub Actions, downloads UF2 files, then installs left half
first and right half second. The macOS installer watches `/Volumes`, prompts the
user to connect each half and double-click reset, copies the matching `.uf2` to
the bootloader volume, syncs, tries to eject, and prints/notifies completion.

## Install Existing Firmware Only

If `firmware/*.uf2` already exists and the user only wants to flash:

```bash
./scripts/install-uf2-macos.py --firmware-dir firmware
```

Use `--preflight` to validate left/right firmware file detection without
waiting for hardware.

## Safety

- Do not use Docker or Colima for this project unless the user explicitly asks.
- Do not create `firmware.zip`; the desired outputs are the two `.uf2` files.
- Do not erase or format volumes. Only copy the matching UF2 file to the newly
  mounted bootloader volume and eject it.
- Wait for explicit user action via the script prompts before each half.
