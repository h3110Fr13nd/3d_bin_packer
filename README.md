# Simple 3D Bin Packing

This library provides a simple implementation of the 3D Bin Packing problem, which is useful for solving the Container Loading Problem (CLP).

## Installation

To install the library, you can use pip:

```sh
pip install 3d_bin_packer
```
## Usage
Importing the Library
```python
from bin_packer import Bin, Item, Packer
```
Creating an instance of the BinPacking class
```python
bin1 = Bin('Le grande box', 100, 100, 300)
item1 = Item('Item 1', 150, 50, 50)
```
Packing Items into Bins
To pack items into bins, you need to create a Packer instance, add bins and items to it, and then call the pack method:

```python
packer = Packer()
packer.add_bin(bin1)
packer.add_item(item1)
packer.pack()
```
Checking the Results
You can check the packed items and unfit items using the bins and unfit_items properties of the Packer class:

```python
for bin_ in packer.bins:
    print(f"Bin: {bin_.name}")
    for item in bin_.items:
        print(f"  Packed item: {item.name}")

print("Unfit items:")
for item in packer.unfit_items:
    print(f"  Unfit item: {item.name}")
```

Example
Here is a complete example that demonstrates how to use the library:

```python
from bin_packer import Packer, Bin, Item

# Create bins
bin1 = Bin('Le grande box', 100, 100, 300)

# Create items
items = [Item('Item 1', 150, 50, 50) for i in range(1000)]

# Create packer and add bins and items
packer = Packer()
packer.add_bin(bin1)
for item in items:
    packer.add_item(item)

# Pack items into bins
packer.pack()

# Check the results
for bin_ in packer.bins:
    print(f"Bin: {bin_.name}")
    for item in bin_.items:
        print(f"  Packed item: {item.name}")
        print(f"    Position: {item.position}")


print("Unfit items:", len(packer.unfit_items))
```
Running Tests
To run the tests, you can use the unittest module:

```sh
python -m unittest discover tests
```
License
This project is licensed under the MIT License. See the LICENSE file for details.
