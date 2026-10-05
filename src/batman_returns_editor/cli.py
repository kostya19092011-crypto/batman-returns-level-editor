from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Sequence

from .data_model import LevelData, LevelObject


class BatmanReturnsROMParser:
    """A practical ROM parser for extracting tile-based stage layouts.

    The exact Batman Returns Game Gear level format is proprietary and requires
    reverse engineering from a real ROM dump. This class provides a safe and
    extensible foundation for identifying candidate level blocks, reading raw
    tile arrays, and exporting a stage to JSON so it can be edited externally.
    """

    def __init__(self, rom_path: str | Path):
        self.rom_path = Path(rom_path)
        if not self.rom_path.exists():
            raise FileNotFoundError(f"ROM not found: {self.rom_path}")
        self.rom_bytes = self.rom_path.read_bytes()

    def scan_candidate_level_offsets(
        self,
        signature: bytes = b"BATM",
        max_results: int = 32,
    ) -> List[int]:
        """Find likely stage markers in the ROM.

        This is intentionally conservative: it is only a search helper for a
        real reverse-engineering session. Once the actual level table is found,
        the offsets can be replaced by a more precise table-driven scan.
        """
        offsets: List[int] = []
        limit = len(self.rom_bytes) - len(signature)
        for idx in range(limit):
            if self.rom_bytes[idx : idx + len(signature)] == signature:
                offsets.append(idx)
                if len(offsets) >= max_results:
                    break
        return offsets

    def build_level_from_offset(
        self,
        offset: int,
        width: int = 16,
        height: int = 12,
        name: str = "level_0",
    ) -> LevelData:
        payload = self.rom_bytes[offset:]
        tile_count = width * height
        if len(payload) < tile_count:
            raise ValueError(
                f"Not enough bytes for a {width}x{height} map at offset 0x{offset:x}."
            )

        tiles: List[List[int]] = []
        for row_index in range(height):
            row = []
            base = row_index * width
            for col_index in range(width):
                value = payload[base + col_index]
                row.append(value)
            tiles.append(row)

        return LevelData(
            name=name,
            width=width,
            height=height,
            tiles=tiles,
            objects=[LevelObject(x=3, y=5, type="enemy", subtype="guard", flags=0)],
            palette=[0, 1, 2, 3],
            checksum=self._checksum(tiles),
        )

    def export_level(
        self,
        offset: int,
        out_path: str | Path,
        width: int = 16,
        height: int = 12,
        name: str = "level_0",
    ) -> Path:
        level = self.build_level_from_offset(offset, width=width, height=height, name=name)
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(level.to_dict(), indent=2), encoding="utf-8")
        return out

    @staticmethod
    def _checksum(tiles: Sequence[Sequence[int]]) -> int:
        total = 0
        for row in tiles:
            for value in row:
                total += int(value)
        return total


def build_level_from_bytes(
    payload: bytes,
    width: int = 16,
    height: int = 12,
    name: str = "level_0",
) -> LevelData:
    """Build a LevelData object from raw bytes without a ROM file."""
    tile_count = width * height
    if len(payload) < tile_count:
        raise ValueError(f"Payload is too short for a {width}x{height} level.")

    tiles: List[List[int]] = []
    for row in range(height):
        row_values = []
        for col in range(width):
            row_values.append(payload[row * width + col])
        tiles.append(row_values)

    return LevelData(
        name=name,
        width=width,
        height=height,
        tiles=tiles,
        objects=[LevelObject(x=3, y=5, type="enemy", subtype="guard", flags=0)],
        palette=[0, 1, 2, 3],
        checksum=sum(value for row in tiles for value in row),
    )
