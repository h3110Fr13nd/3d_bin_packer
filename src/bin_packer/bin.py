from typing import List, Tuple
from .log import create_logger
from .box import Box

log = create_logger('3D: ')

class Bin(Box):
    def __init__(self, name: str, w: float, h: float, d: float):
        super().__init__(name, w, h, d)
        self._items = []

    @property
    def items(self) -> List:
        return self._items

    @items.setter
    def items(self, items: List) -> None:
        self._items = items

    def score_rotation(self, item, rotation_type: int) -> float:
        """
        Calculate a score for a given item and rotation type.

        Scores are higher for rotations that closest match item dimensions to Bin dimensions.
        For example, rotating the item so the longest side is aligned with the longest Bin side.

        Example (Bin is 11 x 8.5 x 5.5, Item is 8.1 x 5.2 x 5.2):
         Rotation 0:
           8.1 / 11  = 0.736
           5.2 / 8.5 = 0.612
           5.2 / 5.5 = 0.945
           -----------------
           0.736 ** 2 + 0.612 ** 2 + 0.945 ** 2 = 1.809

         Rotation 1:
           8.1 / 8.5 = 0.953
           5.2 / 11 = 0.473
           5.2 / 5.5 = 0.945
           -----------------
           0.953 ** 2 + 0.473 ** 2 + 0.945 ** 2 = 2.025
        """
        item.rotation_type = rotation_type
        d = item.dimension

        # If the item doesn't fit in the Bin
        if self.width < d[0] or self.height < d[1] or self.depth < d[2]:
            return 0

        # Square the results to increase the impact of high values (e.g. > 0.8)
        width_score = pow(d[0] / self.width, 2)
        height_score = pow(d[1] / self.height, 2)
        depth_score = pow(d[2] / self.depth, 2)

        return width_score + height_score + depth_score

    def get_best_rotation_order(self, item) -> List[int]:
        """
        Calculate the best rotation order for a given Item based on score_rotation().
        Returns rotation types sorted by their score, DESC
        """
        rotation_scores = {}
        
        # Score all rotation types
        for rotation in item.allowed_rotations:
            rotation_scores[rotation] = self.score_rotation(item, rotation)

        # Sort the rotation types by score in descending order
        return sorted(rotation_scores.keys(), 
                     key=lambda x: rotation_scores[x], 
                     reverse=True)

    def put_item(self, item, p: Tuple[float, float, float]) -> bool:
        """
        Attempt to place an item in the bin at the specified position.
        Returns True if the item fits, False otherwise.
        """
        fit = False
        rotations = self.get_best_rotation_order(item)
        item.position = p

        for rotation in rotations:
            item.rotation_type = rotation
            d = item.dimension

            if (self.width < p[0] + d[0] or 
                self.height < p[1] + d[1] or 
                self.depth < p[2] + d[2]):
                fit = False
            else:
                fit = True
                for other_item in self.items:
                    if other_item.does_intersect(item):
                        fit = False
                        break
                
                if fit:
                    self.items.append(item)

            log(f'try to putItem {fit} item {str(item)} box {str(self)}')
            
            if fit:
                break

        return fit

    def __str__(self) -> str:
        return f'Bin: {self.name} (W x H x D = {self.width} x {self.height} x {self.depth})'