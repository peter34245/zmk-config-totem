# GitHub Actions Firmware Builds

This project can build firmware through GitHub Actions without running Docker,
Colima, or a local ZMK toolchain.

The workflow in `.github/workflows/build.yml` builds the entries in `build.yaml`
and publishes a GitHub Actions artifact named `firmware`.

## Download Behavior

GitHub stores the artifact as a ZIP internally, but `gh run download` extracts it
for you. This project's helper downloads the artifact contents into:

```text
firmware/
```

Expected files:

```text
firmware/totem_left-seeeduino_xiao_ble-zmk.uf2
firmware/totem_right-seeeduino_xiao_ble-zmk.uf2
```

The helper does not create `firmware.zip`.

## Build Current Branch And Download UF2 Files

From this repo:

```sh
./scripts/build-firmware-github.sh
```

If there are no new commits to push, the script triggers the workflow manually
for the current branch.

If you have uncommitted firmware source edits, pass a commit message. By
default the script commits changes under `config`, `build.yaml`, and
`.github/workflows`, pushes the current branch, waits for the matching Actions
run, and downloads the `firmware` artifact into `firmware/`.

```sh
./scripts/build-firmware-github.sh "Update keymap"
```

## Build And Install

To build with GitHub Actions and then flash the left and right halves:

```sh
./scripts/build-and-install.sh "Update keymap"
```

The installer waits for each keyboard half to appear as a mounted UF2 bootloader
volume under `/Volumes`, copies the matching `.uf2` file, syncs, and ejects the
volume if it has not already disappeared.

## Requirements

- GitHub CLI: `gh`
- Authenticated GitHub account with access to this repo
- Network access
- macOS for the install script
