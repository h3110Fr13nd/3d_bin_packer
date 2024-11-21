# packer.py

from typing import List, Optional, Union
from .item import START_POSITION, Axis
from .bin import Bin
from .item import Item

class Packer:
    def __init__(self):
        """Initialize the packer with empty bins, items, and unfit items lists."""
        self._bins: List[Bin] = []
        self._items: List[Item] = []
        self._unfit_items: List[Item] = []

    @property
    def bins(self) -> List[Bin]:
        """Get list of bins."""
        return self._bins

    @property
    def items(self) -> List[Item]:
        """Get list of items to be packed."""
        return self._items

    @property
    def unfit_items(self) -> List[Item]:
        """Get list of items that couldn't be packed."""
        return self._unfit_items

    def add_bin(self, bin_: Bin) -> None:
        """Add a bin to the packer."""
        self._bins.append(bin_)

    def add_item(self, item: Item) -> None:
        """Add an item to be packed."""
        self._items.append(item)

    def find_fitted_bin(self, item: Item) -> Optional[Bin]:
        """
        Find the first bin that the item fits in.
        
        Args:
            item: Item to find a bin for
            
        Returns:
            Optional[Bin]: Bin that fits the item, or None if no bin fits
        """
        for bin_ in self._bins:
            if not bin_.put_item(item, START_POSITION):
                continue
            
            if len(bin_.items) == 1 and bin_.items[0] == item:
                bin_.items = []
            
            return bin_
        return None

    def get_bigger_bin_than(self, other_bin: Bin) -> Optional[Bin]:
        """
        Find the first bin that's bigger than the given bin.
        
        Args:
            other_bin: Bin to compare against
            
        Returns:
            Optional[Bin]: First bin with larger volume, or None if none found
        """
        return next((b for b in self._bins if b.volume > other_bin.volume), None)

    def unfit_item(self) -> None:
        """Move the first item to the unfit items list."""
        if not self.items:
            return
        self.unfit_items.append(self.items.pop(0))

    def pack_to_bin(self, bin_: Bin, items: List[Item]) -> List[Item]:
        """
        Pack items into the given bin.
        
        Args:
            bin_: Bin to pack items into
            items: Items to pack
            
        Returns:
            List[Item]: Items that couldn't be packed
        """
        b2 = None
        unpacked = []
        
        # Try to fit the first item
        fit = bin_.put_item(items[0], START_POSITION)
        if not fit:
            b2 = self.get_bigger_bin_than(bin_)
            if b2:
                return self.pack_to_bin(b2, items)
            return self.items

        # Pack remaining items
        for item in self.items[1:]:
            fitted = False
            
            # Try different axes for positioning
            for axis in [Axis.width, Axis.height, Axis.depth]:
                if fitted:
                    break
                    
                for item_b in bin_.items:
                    if axis == Axis.width:
                        item_position = [
                            item_b.position[0] + item_b.dimension[0],
                            item_b.position[1],
                            item_b.position[2]
                        ]
                    elif axis == Axis.height:
                        item_position = [
                            item_b.position[0],
                            item_b.position[1] + item_b.dimension[1],
                            item_b.position[2]
                        ]
                    else:  # Axis.depth
                        item_position = [
                            item_b.position[0],
                            item_b.position[1],
                            item_b.position[2] + item_b.dimension[2]
                        ]

                    if bin_.put_item(item, item_position):
                        fitted = True
                        break

            if not fitted:
                while b2 is not None:
                    b2 = self.get_bigger_bin_than(bin_)
                    if b2:
                        b2.items.append(item)
                        left = self.pack_to_bin(b2, b2.items)
                        if not left:
                            bin_ = b2
                            fitted = True
                            break

                if not fitted:
                    unpacked.append(item)

        return unpacked

    def pack(self) -> None:
        """Pack all items into bins."""
        # Sort bins smallest to largest
        self._bins.sort(key=lambda x: x.volume)
        
        # Sort items largest to smallest
        self._items.sort(key=lambda x: x.volume, reverse=True)
        
        while self._items:
            bin_ = self.find_fitted_bin(self._items[0])
            if not bin_:
                self.unfit_item()
                continue
            
            self._items = self.pack_to_bin(bin_, self._items)