# Project Instructions

This repository is the user's TOTEM ZMK keymap project.

When the user types `/build`, invokes `$build`, or asks to build/install
firmware:

1. Use the repo-local `build` skill from `.agents/skills/build`.
2. Prefer project scripts over reimplementing the workflow.
3. Build firmware with GitHub Actions, not local Docker/Colima, unless the user
   explicitly asks for local builds.
4. Download only `.uf2` files into `firmware/`; do not create `firmware.zip`.
5. Install left half first, then right half, using `scripts/install-uf2-macos.py`.

Default command for `/build`:

```sh
./scripts/build-and-install.sh "Update keymap"
```

Use `./scripts/build-firmware-github.sh "Update keymap"` when the user asks
for build/download only. Use `./scripts/install-uf2-macos.py --firmware-dir
firmware` when the user already has current UF2 files and only wants to flash.

Primary user-edited keymap file:

```text
config/totem.keymap
```
