# Reverse-engineering notes for Batman Returns (Game Gear)

This document captures the research workflow and the expected next steps for building a true ROM-based level editor for Batman Returns on the Sega Game Gear.

## 1. Goal

Build an editor that can:

- read a Game Gear ROM dump
- identify level data blocks
- decode tiles, collisions, enemies, and stage objects
- render a map preview
- export modified levels back to a valid binary structure

## 2. Required data to recover

For a real implementation, the following must be recovered from the ROM:

- absolute offsets for level tables
- bank-switching behavior
- level dimensions and tile map layout
- palette assignments
- object placement tables
- collision or platform flags
- any compression or run-length encoding

## 3. Typical Game Gear reverse-engineering path

1. Open the ROM in a hex editor and identify the header structure.
2. Search for known tile values or marker sequences.
3. Locate a level table and trace pointer references.
4. Dump a single level section and identify its dimensions.
5. Reverse the pattern for collision/tiles and build a parser.
6. Validate the parser against known screen layouts.
7. Export editable JSON or a tile atlas for editing.
8. Repack the level back into the original binary format.

## 4. Likely technical areas

- 8-bit tile indices and palette banks
- 2-byte object descriptors for enemies and pickups
- 16-bit pointer arrays to level data
- scrolling stage definitions and background tiles
- DMA or memory-mapped VRAM layout for Game Gear

## 5. The current project structure

The repository intentionally makes the reverse-engineering process modular:

- `rom_parser.py` handles binary extraction and scanning
- `data_model.py` defines editable structures
- `cli.py` exposes a command-line entry point
- `examples/sample_level.json` provides a sample structured map

These modules allow a researcher to iterate on the real format without needing a full GUI or a full reimplementation of the game engine.

## 6. Recommended next step

The next practical task is to dump a real Batman Returns ROM and inspect the level table area. Once a known level is isolated, the parser can be hardened to exact offsets and tile encoding.

This is an ideal place to build a clean editor foundation before tackling the full binary repacker.
