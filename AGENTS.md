# Project Instructions

This repository is the user's personal TOTEM ZMK keymap project. Treat these
files as agent-facing workflow instructions, not user documentation.

## Repository Facts

- Keyboard: TOTEM split keyboard with `seeeduino_xiao_ble` controllers.
- Primary editable keymap: `config/totem.keymap`.
- Build matrix: `build.yaml`.
- ZMK manifest: `config/west.yml`.
- Firmware output directory: `firmware/`.

## Source Of Truth

- Edit only `config/totem.keymap` for layout changes.
- Keep every keymap layer at exactly 38 bindings.
- Treat this as a 34-key user layout on 38-key TOTEM firmware shape: physical
  key positions `20 32 37 31` are intentionally unused by the user. Keep their
  binding slots present as needed for ZMK/keymap shape, but do not assign core
  typing, layer, or shortcut behavior there unless the user explicitly asks.
- Keep keymap layer node names parser-friendly for Nick Coutsos' keymap editor:
  start with a letter or underscore, use underscores instead of hyphens, and
  avoid names that begin with digits.
- Prefer layer node names in the form `<purpose>_layer_<number>`, where
  `<number>` matches the layer's actual zero-based order in `keymap`.
- Do not recreate `config/boards/shields/totem/totem.keymap`; this project uses
  the top-level user keymap instead.
- Leave `firmware/` outputs untracked.

## Layout Context

- `asergo` is the user's primary custom layout. The user does not use QWERTY as
  their normal typing layout, so do not infer intended key positions from QWERTY
  when changing typing-layer behavior.
- Treat `base_layer` as a QWERTY-compatible alternate/reference layer, not the
  user's preferred layout.
- The user's practical layout uses 34 active keys. Positions `20 32 37 31` are
  outside the intended active layout even though each ZMK layer still has 38
  binding slots.
- The `asergo` name comes from the home-row sequence `A S E R G`, with an added
  `O` for the playful `aser go` name.

## Layer References

- ZMK behavior references such as `&lt`, `&mo`, `&sl`, and `&tog` use numeric
  layer indexes, not layer node names. After reordering, inserting, deleting, or
  renaming layers, audit every numeric layer reference.
- Use comments for trigger details when helpful, for example the held key or
  physical key position that activates a layer. Do not put physical key
  positions in layer names unless the same logical layer has multiple triggers
  that would otherwise be ambiguous.
- Conditional layers are for layer-state combinations: when multiple layers are
  active together, ZMK activates another layer automatically. Prefer ordinary
  behaviors or combos when the trigger is a specific key or key combo. If adding
  conditional layers, keep `then-layer` higher priority than the `if-layers` and
  document the relationship near the declaration.

## Gaming Workflow

- `gaming_layer_3` is the low-latency game mode. Keep movement, held
  modifiers, zoom/client keys, and jump as plain `&kp` bindings.
- `gaming_plus_layer_4` is the held hotbar/util layer reached from the gaming
  thumb key. Its current key placement is intentional and user-tuned; do not
  redesign or "optimize" this layer unless the user explicitly asks.
- `gaming_plus_oneshot_layer_5` is for one-shot function keys such as `F3` and
  `F5`.
- Keep normal productivity combos scoped away from layers `3 4 5`; combos on
  game-critical physical positions can add timeout latency or fire accidental
  shortcuts during games.

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
