"""
Modul obsahující definici testovacích případů pro třídu Bag.
"""

import unittest
from ..bag import Bag
from ..item import Item

class BagTests(unittest.TestCase):
    """
    Třída obsahující metody pro testování třídy Bag.
    """

    def setUp(self) -> None:
        """
        Metoda pro nastavení test fixture.
        """
        self.test_bag = Bag(("_test item 1", "_test item 2"))
        self.test_bag.initialize()
        return super().setUp()
    
    def test_item_method(self):
        """
        Funkce pro otestování funkce item().
        """
        item_1 = self.test_bag.item("test item 1")
        item_2 = self.test_bag.item("test item 2")
        item_3 = self.test_bag.item("Non existing item")
        self.assertIsNotNone(item_1)
        self.assertIsNotNone(item_2)
        self.assertIsNone(item_3)

    def test_init(self):
        """
        Metoda pro testování metody __init__.
        """
        item_1 = self.test_bag.item("test item 1")
        item_2 = self.test_bag.item("test item 2")
        self.assertIsNotNone(item_1)
        self.assertIsNotNone(item_2)
    
    def test_add_item(self):
        """
        Metoda pro otestování metody add_item.
        """
        bag_items_before_add = self.test_bag.items.copy()
        self.test_bag.add_item(Item("_test item 3"))
        bag_items_after = self.test_bag.items
        self.assertNotEqual(bag_items_before_add, bag_items_after)

    def test_remove_item(self):
        """
        Metoda pro testování metody remove_item.
        """
        bag_items_before_remove = self.test_bag.items.copy()
        initial_content = self.test_bag.content
        self.test_bag.remove_item("test item 1")
        content_after_remove = self.test_bag.content
        self.assertEqual(initial_content - 1, content_after_remove)
        self.assertNotEqual(bag_items_before_remove, self.test_bag.items)
        wrong_name_removal = self.test_bag.remove_item("test item 3")
        self.assertIsNone(wrong_name_removal)