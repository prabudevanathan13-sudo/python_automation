
import unittest
class Item(unittest.TestCase):
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity


# Create items
item1 = Item("Milk", 60, 2)
item2 = Item("Bread", 40, 1)
item3 = Item("Eggs", 7, 10)
# Calculate total
grand_total = item1.total_price() + item2.total_price() + item3.total_price()

print("Total Amount =", grand_total)
