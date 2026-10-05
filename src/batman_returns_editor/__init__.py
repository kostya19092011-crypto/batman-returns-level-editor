#!/usr/bin/env python3

import argparse
from pathlib import Path

from batman_returns_editor import BatmanReturnsROMParser


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batman Returns Sega Game Gear level editor")
    parser.add_argument("--rom", required=True, help="Path to a Game Gear ROM dump")
    parser.add_argument("--scan", action="store_true", help="Scan the ROM for candidate level markers")
    parser.add_argument("--index", type=int, default=0, help="Offset index to export from the scan list")
    parser.add_argument("--offset", type=lambda value: int(value, 0), default=None, help="Raw ROM offset in hex or decimal")
    parser.add_argument("--width", type=int, default=16, help="Level width in tiles")
    parser.add_argument("--height", type=int, default=12, help="Level height in tiles")
    parser.add_argument("--export", help="Path for the exported JSON level")
    parser.add_argument("--name", default="level_0", help="Friendly name for the level")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parser = BatmanReturnsROMParser(args.rom)

    if args.scan:
        offsets = parser.scan_candidate_level_offsets()
        if not offsets:
            print("No candidate level markers were found.")
            return
        print(f"Detected candidate level markers: {offsets}")
        return

    if args.offset is not None:
        target_offset = args.offset
        if args.export:
            parser.export_level(
                target_offset,
                args.export,
                width=args.width,
                height=args.height,
                name=args.name,
            )
            print(f"Exported level from offset 0x{target_offset:x} to {args.export}")
            return
        level = parser.build_level_from_offset(target_offset, width=args.width, height=args.height, name=args.name)
        print(level.render_ascii())
        return

    if args.export:
        parser.export_level(
            args.index,
            args.export,
            width=args.width,
            height=args.height,
            name=args.name,
        )
        print(f"Exported level at index {args.index} to {args.export}")
        return

    print("No action selected. Use --scan, --offset, or --export.")


if __name__ == "__main__":
    main()












