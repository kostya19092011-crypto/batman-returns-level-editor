# Batman Returns Level Editor for Sega Game Gear

A practical reverse-engineering starter project for editing Batman Returns level layouts from a Sega Game Gear ROM dump.

This repository is intentionally structured as a ROM-hacking tool prototype: it can scan candidate level blocks in a ROM, decode the raw tile data into a readable level structure, export it to JSON, and provide a clean foundation for direct binary patching or a GUI editor later.

## What this project includes

- ROM scan utilities for candidate level offsets
- Generic level parser for Game Gear tile arrays
- Level data model with tiles, objects, palettes, and metadata
- CLI for exporting levels to JSON
- Documentation for reverse-engineering workflow

## Project status

This is a serious starter prototype, not a full 1:1 ROM mapping of the original game. Batman Returns uses a proprietary binary format and the exact level layout tables must be recovered from a real ROM dump. This code gives you the tooling and project structure so the reverse-engineering work can move quickly.

## Repository structure

- `src/batman_returns_editor/` — Python editor core
- `examples/` — sample JSON levels
- `docs/REVERSE_ENGINEERING_NOTES.md` — engineering notes and method

## Quick start

1. Install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Scan a ROM dump for candidate level blocks:

   ```bash
   python -m batman_returns_editor.cli --rom /path/to/batman_returns.gg --scan
   ```

3. Export a level as JSON:

   ```bash
   python -m batman_returns_editor.cli --rom /path/to/batman_returns.gg --index 0 --export output/level_0.json
   ```

## Example output

The exported JSON contains a human-readable level definition:

```json
{
  "name": "level_0",
  "width": 16,
  "height": 12,
  "tiles": [[0, 0, 0, 0], [0, 1, 2, 0]],
  "objects": [
    {"x": 3, "y": 5, "type": "enemy", "subtype": "guard", "flags": 0}
  ],
  "palette": [0, 1, 2, 3],
  "checksum": 0
}
```

## Notes for ROM hacking

To turn this into a true Batman Returns level editor, the next step is to recover:

- exact ROM offsets for level tables
- tile index scheme and palette assignments
- collision/block metadata
- NPC/enemy/object placement table
- compression or bank switching rules

This project is intended to be the foundation for that work.

## License

This project is provided as a research and tooling repository for hobbyist ROM editing. No original game assets are included.
