from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Tile:
    tile_id: int
    palette: int = 0
    flip_x: bool = False
    flip_y: bool = False
    priority: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tile_id": self.tile_id,
            "palette": self.palette,
            "flip_x": self.flip_x,
            "flip_y": self.flip_y,
            "priority": self.priority,
        }


@dataclass
class LevelObject:
    x: int
    y: int
    type: str
    subtype: str
    flags: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "subtype": self.subtype,
            "flags": self.flags,
        }


@dataclass
class LevelData:
    name: str
    width: int
    height: int
    tiles: List[List[int]] = field(default_factory=list)
    objects: List[LevelObject] = field(default_factory=list)
    palette: List[int] = field(default_factory=list)
    checksum: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "tiles": self.tiles,
            "objects": [obj.to_dict() for obj in self.objects],
            "palette": self.palette,
            "checksum": self.checksum,
        }

    def render_ascii(self) -> str:
        lines = []
        for row in self.tiles:
            lines.append(" ".join(f"{tile:02x}" for tile in row))
        return "\n".join(lines)
