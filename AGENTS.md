# Project Instructions

This repository is the user's personal TOTEM ZMK keymap project. Treat these
files as agent-facing workflow instructions, not user documentation.

## Source Of Truth

- Edit only `config/totem.keymap` for layout changes.
- Keep every keymap layer at exactly 38 bindings.
- Do not recreate `config/boards/shields/totem/totem.keymap`; this project uses
  the top-level user keymap instead.
- Leave `firmware/` outputs untracked.

## Build Skill

When the user types `/build`, invokes `$build`, asks to build firmware, asks to
download UF2 artifacts, or asks to install/flash the keyboard halves:

1. Use the repo-local `build` skill from `.agents/skills/build`.
2. Follow the skill's `SKILL.md` for the full workflow.
3. Prefer project scripts over reimplementing build, download, or install
   steps.

Default command for build and install:

```sh
./scripts/build-and-install.sh "Update keymap"
```

Build/download only:

```sh
./scripts/build-firmware-github.sh "Update keymap"
```

Install existing firmware only:

```sh
./scripts/install-uf2-macos.py --firmware-dir firmware
```

## Firmware Workflow

- Build firmware with GitHub Actions, not local Docker or Colima, unless the
  user explicitly asks for local builds.
- Download only extracted `.uf2` files into `firmware/`; do not create
  `firmware.zip`.
- Install left half first, then right half.
- Use `GITHUB_BUILD.md` only as supporting detail for the GitHub Actions helper
  scripts; `AGENTS.md` and the `build` skill are the routing source of truth.
