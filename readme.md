# TOTEM ZMK Agent Context

This repository is a personal ZMK config for a 38-key TOTEM split keyboard using
`seeeduino_xiao_ble` controllers.

This file is context for AI agents. The operational instructions live in:

- `AGENTS.md` for agent routing and source-of-truth rules.
- `.agents/skills/build/SKILL.md` for build, download, and install execution.
- `GITHUB_BUILD.md` for details behind the GitHub Actions firmware helper.

Key facts:

- Primary editable keymap: `config/totem.keymap`
- Expected layer size: 38 bindings per layer
- Build matrix: `build.yaml`
- ZMK manifest: `config/west.yml`
- Firmware output directory: `firmware/`

Agents should not recreate a shield-level `totem.keymap`; this project uses the
top-level user keymap.
