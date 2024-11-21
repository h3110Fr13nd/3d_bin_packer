import unittest
from src.bin_packer import Packer, Bin, Item

class TestPacker(unittest.TestCase):

    def setUp(self):
        self.test_datas = [
            {
                "name": "Edge case that needs rotation.",
                "bins": [
                    Bin('Le grande box', 100, 100, 300),
                ],
                "items": [
                    Item('Item 1', 150, 50, 50),
                ],
                "expectation": lambda packer: len(packer.bins[0].items) == 1 and len(packer.unfit_items) == 0,
            },
            {
                "name": "Edge case with only rotation 3 and 0 enabled.",
                "bins": [
                    Bin('Le grande box', 100, 100, 300),
                ],
                "items": [
                    Item('Item 1', 150, 50, 50),
                ],
                "expectation": lambda packer: len(packer.bins[0].items) == 1 and len(packer.unfit_items) == 0,
            },
            {
                "name": "Test three items fit into smaller bin after being rotated.",
                "bins": [
                    Bin("1. Le petite box", 296, 296, 8),
                    Bin("2. Le grande box", 2960, 2960, 80),
                ],
                "items": [
                    Item("Item 1", 250, 250, 2),
                    Item("Item 2", 250, 2, 250),
                    Item("Item 3", 2, 250, 250),
                ],
                "expectation": lambda packer: (
                    packer.bins[0].name == '1. Le petite box' and
                    len(packer.bins[0].items) == 3 and
                    len(packer.bins[1].items) == 0 and
                    len(packer.unfit_items) == 0
                ),
            },
            {
                "name": "Test three items fit into larger bin.",
                "bins": [
                    Bin("1. Le petite box", 296, 296, 8),
                    Bin("2. Le grande box", 2960, 2960, 80),
                ],
                "items": [
                    Item("Item 1", 2500, 2500, 20),
                    Item("Item 2", 2500, 2500, 20),
                    Item("Item 3", 2500, 2500, 20),
                ],
                "expectation": lambda packer: (
                    packer.bins[0].name == '1. Le petite box' and
                    len(packer.bins[0].items) == 0 and
                    len(packer.bins[1].items) == 3 and
                    len(packer.unfit_items) == 0
                ),
            },
            {
                "name": "1 bin with 7 items fit into.",
                "bins": [
                    Bin("Bin 1", 220, 160, 100),
                ],
                "items": [
                    Item("Item 1", 20, 100, 30),
                    Item("Item 2", 100, 20, 30),
                    Item("Item 3", 20, 100, 30),
                    Item("Item 4", 100, 20, 30),
                    Item("Item 5", 100, 20, 30),
                    Item("Item 6", 100, 100, 30),
                    Item("Item 7", 100, 100, 30),
                ],
                "expectation": lambda packer: len(packer.bins[0].items) == 7 and len(packer.unfit_items) == 0,
            },
            {
                "name": "Big item is packed first.",
                "bins": [
                    Bin("Bin 1", 100, 100, 100),
                ],
                "items": [
                    Item("Item 1", 50, 100, 100),
                    Item("Item 2", 100, 100, 100),
                    Item("Item 3", 50, 100, 100),
                ],
                "expectation": lambda packer: len(packer.bins[0].items) == 1 and len(packer.unfit_items) == 2,
            },
            {
                "name": "Larger items are tried first.",
                "bins": [
                    Bin("Small Bin", 50, 100, 100),
                    Bin("Bigger Bin", 150, 100, 100),
                    Bin("Small Bin", 50, 100, 100),
                ],
                "items": [
                    Item("Item 1 Small", 50, 100, 100),
                    Item("Item 3 Small", 50, 100, 100),
                    Item("Item 3 Small", 50, 100, 100),
                    Item("Item 2 Big", 100, 100, 100),
                ],
                "expectation": lambda packer: (
                    packer.bins[2].name == 'Bigger Bin' and
                    len(packer.bins[2].items) == 2 and
                    packer.bins[0].name == 'Small Bin' and
                    len(packer.bins[0].items) == 1 and
                    len(packer.unfit_items) == 0
                ),
            },
            {
                "name": "First item fits without rotation but needs to be rotated to fit all items.",
                "bins": [
                    Bin('USPS Medium Flat Rate Box (Top Loading)', 11, 8.5, 5.5),
                ],
                "items": [
                    Item('Item 1', 8.1, 5.2, 2.2),
                    Item('Item 2', 8.1, 5.2, 3.3),
                ],
                "expectation": lambda packer: len(packer.bins[0].items) == 2 and len(packer.unfit_items) == 0,
            },
            {
                "name": "Floating point arithmetic is handled correctly.",
                "bins": [
                    Bin("Bin 1", 12, 12, 5.5),
                ],
                "items": [
                    Item("Item 1", 12, 12, 0.005),
                    Item("Item 2", 12, 12, 0.005),
                ],
                "expectation": lambda packer: len(packer.bins[0].items) == 2 and len(packer.unfit_items) == 0,
            },
        ]

    def test_packer(self):
        for test_data in self.test_datas:
            with self.subTest(test_data["name"]):
                packer = Packer()
                for bin_ in test_data["bins"]:
                    packer.add_bin(bin_)
                for item in test_data["items"]:
                    packer.add_item(item)
                packer.pack()
                self.assertTrue(test_data["expectation"](packer))

if __name__ == "__main__":
    unittest.main()
