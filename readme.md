# ZMK Config For The TOTEM Split Keyboard

This is the personal ZMK config for a 38-key
[TOTEM](https://github.com/GEIGEIGEIST/totem) split keyboard using
`seeeduino_xiao_ble` controllers.

The primary editable keymap is:

```text
config/totem.keymap
```

Do not edit `config/boards/shields/totem/totem.keymap` for daily layout
changes. That file belongs to the local shield definition and is kept only as a
reference/default keymap.

## Editing The Keymap

Use one of these workflows:

- Edit `config/totem.keymap` directly in an IDE.
- Ask an AI agent to edit `config/totem.keymap`.
- Use [Keymap Editor](https://github.com/nickcoutsos/keymap-editor) with the
  file system source and choose `config/totem.keymap`.

After editing, build through GitHub Actions. Local Docker or Colima builds are
not the default workflow for this repo.

## Build And Install

Default local command:

```sh
./scripts/build-and-install.sh "Update keymap"
```

This commits firmware source edits under `config`, `build.yaml`, and
`.github/workflows`, pushes the current branch, waits for GitHub Actions,
downloads the firmware artifact into `firmware/`, then installs the left half
first and the right half second.

Expected downloaded files:

```text
firmware/totem_left-seeeduino_xiao_ble-zmk.uf2
firmware/totem_right-seeeduino_xiao_ble-zmk.uf2
```

The helper downloads extracted `.uf2` files. It does not create or require a
`firmware.zip` file.

## Build Only

Use this when you want to build and download firmware without flashing:

```sh
./scripts/build-firmware-github.sh "Update keymap"
```

## Install Existing Firmware Only

Use this when `firmware/` already contains current left and right UF2 files:

```sh
./scripts/install-uf2-macos.py --firmware-dir firmware
```

Preflight the installer without waiting for keyboard hardware:

```sh
./scripts/install-uf2-macos.py --firmware-dir firmware --preflight
```

## AI Agent Notes

Agents should follow [AGENTS.md](AGENTS.md) and the repo-local build skill in
`.agents/skills/build`. The short rule is:

- Edit `config/totem.keymap`.
- Keep every layer at 38 bindings.
- Build with GitHub Actions via the project scripts.
- Download only `.uf2` files into `firmware/`.
- Flash left half first, then right half.

## Requirements

- GitHub CLI: `gh`
- Authenticated GitHub account with access to this repository
- Network access
- macOS for the install script
