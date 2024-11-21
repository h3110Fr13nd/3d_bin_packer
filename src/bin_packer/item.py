# item.py

from enum import IntEnum
from typing import List, Tuple
from .box import Box

class RotationType(IntEnum):
    whd = 0  # width, height, depth
    hwd = 1  # height, width, depth
    hdw = 2  # height, depth, width
    dhw = 3  # depth, height, width
    dwh = 4  # depth, width, height
    wdh = 5  # width, depth, height

class Axis(IntEnum):
    width = 0
    height = 1
    depth = 2

START_POSITION = [0, 0, 0]

ROTATION_TYPE_STRINGS = {
    RotationType.whd: '(w, h, d)',
    RotationType.hwd: '(h, w, d)',
    RotationType.hdw: '(h, d, w)',
    RotationType.dhw: '(d, h, w)',
    RotationType.dwh: '(d, w, h)',
    RotationType.wdh: '(w, d, h)',
}

def rect_intersect(item1: 'Item', item2: 'Item', x: Axis, y: Axis) -> bool:
    """
    Check if two items intersect in the given plane.
    
    Args:
        item1: First item to check
        item2: Second item to check
        x: First axis to check
        y: Second axis to check
        
    Returns:
        bool: True if items intersect, False otherwise
    """
    d1 = item1.dimension
    d2 = item2.dimension
    
    cx1 = item1.position[x] + d1[x] / 2
    cy1 = item1.position[y] + d1[y] / 2
    cx2 = item2.position[x] + d2[x] / 2
    cy2 = item2.position[y] + d2[y] / 2
    
    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)
    
    return ix < (d1[x] + d2[x]) / 2 and iy < (d1[y] + d2[y]) / 2

class Item(Box):
    def __init__(self, name: str, w: float, h: float, d: float):
        """
        Initialize an Item with name and dimensions.
        
        Args:
            name (str): Name of the item
            w (float): Width of the item
            h (float): Height of the item
            d (float): Depth of the item
        """
        super().__init__(name, w, h, d)
        self._allowed_rotations = [
            RotationType.whd,
            RotationType.hwd,
            RotationType.hdw,
            RotationType.dhw,
            RotationType.dwh,
            RotationType.wdh,
        ]
        self._rotation_type = RotationType.whd
        self._position: List[float] = []  # x, y, z

    @property
    def allowed_rotations(self) -> List[RotationType]:
        """Get allowed rotation types for this item."""
        return self._allowed_rotations

    @property
    def rotation_type(self) -> RotationType:
        """Get current rotation type."""
        return self._rotation_type

    @rotation_type.setter
    def rotation_type(self, type_: RotationType):
        """Set current rotation type."""
        self._rotation_type = type_

    @property
    def position(self) -> List[float]:
        """Get current position."""
        return self._position

    @position.setter
    def position(self, position: List[float]):
        """Set current position."""
        self._position = position

    @property
    def rotation_type_string(self) -> str:
        """Get string representation of current rotation type."""
        return ROTATION_TYPE_STRINGS[self._rotation_type]

    @property
    def dimension(self) -> List[float]:
        """Get dimensions based on current rotation type."""
        if self._rotation_type == RotationType.whd:
            return [self.width, self.height, self.depth]
        elif self._rotation_type == RotationType.hwd:
            return [self.height, self.width, self.depth]
        elif self._rotation_type == RotationType.hdw:
            return [self.height, self.depth, self.width]
        elif self._rotation_type == RotationType.dhw:
            return [self.depth, self.height, self.width]
        elif self._rotation_type == RotationType.dwh:
            return [self.depth, self.width, self.height]
        elif self._rotation_type == RotationType.wdh:
            return [self.width, self.depth, self.height]

    def does_intersect(self, other: 'Item') -> bool:
        """
        Check if this item intersects with another item.
        
        Args:
            other: Item to check intersection with
            
        Returns:
            bool: True if items intersect, False otherwise
        """
        return (rect_intersect(self, other, Axis.width, Axis.height) and
                rect_intersect(self, other, Axis.height, Axis.depth) and
                rect_intersect(self, other, Axis.width, Axis.depth))

    def __str__(self) -> str:
        """String representation of the item."""
        return f"Item: {self.name} ({self.rotation_type_string} = {' x '.join(map(str, self.dimension))})"