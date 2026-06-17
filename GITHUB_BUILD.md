# GitHub Actions Build Notes For Agents

Use this file as supporting detail for the project scripts. For task routing,
follow `AGENTS.md` first. For `/build`, `$build`, build, download, and install
requests, use the repo-local `build` skill in `.agents/skills/build`.

## Workflow

`.github/workflows/build.yml` uses ZMK's reusable user-config build workflow.
`build.yaml` defines the two firmware targets:

```text
seeeduino_xiao_ble + totem_left
seeeduino_xiao_ble + totem_right
```

The expected GitHub Actions artifact is named:

```text
firmware
```

## Helper Behavior

Run this helper for build/download-only requests:

```sh
./scripts/build-firmware-github.sh "Update keymap"
```

The helper:

- Detects the current branch and `origin` GitHub repository.
- Commits firmware source edits under `config`, `build.yaml`, and
  `.github/workflows` when a commit message is provided.
- Pushes the branch.
- Waits for the matching GitHub Actions run.
- Downloads the extracted artifact contents into `firmware/`.

Expected local files after download:

```text
firmware/totem_left-seeeduino_xiao_ble-zmk.uf2
firmware/totem_right-seeeduino_xiao_ble-zmk.uf2
```

Do not create `firmware.zip`. GitHub stores artifacts as ZIP internally, but
`gh run download` extracts them for this workflow.

## Build And Install

For build plus flashing:

```sh
./scripts/build-and-install.sh "Update keymap"
```

This runs the GitHub build helper, then flashes with:

```sh
./scripts/install-uf2-macos.py --firmware-dir firmware
```

The installer is macOS-specific. It watches `/Volumes`, prompts for each half,
copies the matching UF2 to the bootloader volume, syncs, and tries to eject.
Install order is always left half first, then right half.

## Preconditions

- `gh` is installed and authenticated.
- The current branch can be pushed to `origin`.
- Network access is available.
- macOS is required for the install script.
