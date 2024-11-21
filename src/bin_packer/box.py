# box.py

from .utils import factored_integer

class Box:
    def __init__(self, name: str, w: float, h: float, d: float):
        """
        Initialize a Box with name and dimensions.
        
        Args:
            name (str): Name of the box
            w (float): Width of the box
            h (float): Height of the box
            d (float): Depth of the box
        """
        self._name = name
        self._width = factored_integer(w)
        self._height = factored_integer(h)
        self._depth = factored_integer(d)

    @property
    def name(self) -> str:
        """Get the name of the box."""
        return self._name

    @property
    def width(self) -> float:
        """Get the width of the box."""
        return self._width

    @property
    def height(self) -> float:
        """Get the height of the box."""
        return self._height

    @property
    def depth(self) -> float:
        """Get the depth of the box."""
        return self._depth

    @property
    def volume(self) -> float:
        """Calculate and return the volume of the box."""
        return self._width * self._height * self._depth