# Contributing

Contributions that improve Kali/Xfce compatibility, accessibility, documentation,
or theme quality are welcome.

## Development setup

```bash
git clone https://github.com/Ankit-ku-panda/Kali-Omarchy-Xfce.git
cd Kali-Omarchy-Xfce
./tests/smoke-test.sh
```

The smoke test uses an isolated temporary home and does not theme your desktop.

## Pull requests

1. Create a focused branch from `main`.
2. Keep system-changing behavior reversible and avoid privileged operations
   unless they are essential package installation steps.
3. Run `./tests/smoke-test.sh`.
4. Update documentation and `CHANGELOG.md` when user-facing behavior changes.
5. Explain what changed, why, and how it was tested in the pull request.

## Theme contributions

A theme must contain a valid `colors.toml` using the current Omarchy color keys.
Backgrounds must be original or distributable under a compatible license, with
their attribution documented. Never include secrets, executable remote-theme
hooks, or copyrighted wallpaper collections without permission.

## Style

- Shell scripts target Bash and use `set -Eeuo pipefail` where appropriate.
- Python targets Python 3.11+ and uses only the standard library.
- Quote shell variables and validate paths before destructive operations.
- Preserve existing user configuration through the backup/restore system.
