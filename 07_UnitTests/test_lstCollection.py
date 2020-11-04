import unittest
from Product import Product
from LstCollection import LstCollection
from memento import *
import os

class TestLstCollection(unittest.TestCase):

    Product_A = Product(**{
        "created_at": "2020-04-09",
        "description": "description1",
        "image_url": "image_url1.jpg",
        "price": "1000",
        "title": "Milk",
        "updated_at": "2020-05-09",
        "u_id" : "1234"
    })

    Product_B = Product(**{
        "created_at": "2020-05-09",
        "description": "description2",
        "image_url": "image_url2.jpg",
        "price": "90",
        "title": "Nuts",
        "updated_at": "2029-05-09",
        "u_id": "1235"
    })

    Product_C = Product(**{
        "created_at": "2019-04-09",
        "description": "description3",
        "image_url": "image_url3.jpg",
        "price": "55",
        "title": "Yogurt",
        "updated_at": "2019-05-09",
        "u_id": "1236"
    })

    Product_D = Product(**{
        "created_at": "2018-04-09",
        "description": "description4",
        "image_url": "image_url4.jpg",
        "price": "66.6",
        "title": "Ice cream",
        "updated_at": "2029-05-09",
        "u_id": "1237"
    })

    def setUp(self):
        self.test_empty_lst = LstCollection()
        self.data = [TestLstCollection.Product_A, TestLstCollection.Product_B, TestLstCollection.Product_C,
                     TestLstCollection.Product_D]
        self.test_lst = LstCollection(*self.data)
        self.caretaker = Caretaker(self.test_lst)
        self.caretaker.backup("Current collection.")

    def testAdd(self):
        self.test_empty_lst.append(TestLstCollection.Product_A)
        self.assertListEqual([i for i in self.test_empty_lst], [TestLstCollection.Product_A],
                             "Add method works improperly")
        self.test_empty_lst.append(TestLstCollection.Product_B)
        self.assertListEqual([i for i in self.test_empty_lst], [TestLstCollection.Product_A,
                                                                TestLstCollection.Product_B],
                             "Add method works improperly")
        self.test_empty_lst.append(TestLstCollection.Product_A)
        self.assertNotEqual([i for i in self.test_empty_lst],
                            [TestLstCollection.Product_A, TestLstCollection.Product_B],
                            "Add method works improperly")

    def test_sort(self):
        object_atters = [name for name in dir(TestLstCollection.Product_D) if not name.startswith('__')
                    and not name.startswith('_') and name != "input_product"]
        for field in object_atters:
            self.data = sorted(self.data, key=lambda product: str(getattr(product, field)).lower())
            self.test_lst.sort(field)
            self.assertListEqual([i for i in self.test_lst], self.data, "Sort method works improperly")

        self.assertRaises(AttributeError, self.test_lst.sort, "impossible")

    def test_search(self):
        found1 = self.test_lst.search('2020')
        found2 = self.test_lst.search('Ice')
        found3 = self.test_lst.search('description')
        found4 = self.test_lst.search('2.jpg')

        self.assertListEqual(found1, [TestLstCollection.Product_A, TestLstCollection.Product_B],
                             "Search method works improperly")
        self.assertListEqual(found2, [TestLstCollection.Product_D], "Search method works improperly")
        self.assertListEqual(found3, self.data, "Search method works improperly")
        self.assertNotEqual(found4, TestLstCollection.Product_B, "Search method works improperly")

    def test_delete(self):
        id1, id2, id3 = "1237", "1236", "1235"
        self.test_lst.delete(id1)
        self.assertListEqual([i for i in self.test_lst], [TestLstCollection.Product_A, TestLstCollection.Product_B,
                                                          TestLstCollection.Product_C],
                             "Delete method works improperly")

        self.test_lst.delete(id2)
        self.assertListEqual([i for i in self.test_lst], [TestLstCollection.Product_A, TestLstCollection.Product_B],
                             "Delete method works improperly")

        self.test_lst.delete(id3)
        self.assertNotEqual([i for i in self.test_lst], [TestLstCollection.Product_A, TestLstCollection.Product_C],
                            "Delete method works improperly")

        self.assertRaises(NameError, self.test_lst.delete, "impossible")

    def test_edit(self):
        to_edit1 = ("1237", "updated_at", "2019-05-09")
        to_edit2 = ("1237", "created_at", "2010-06-09")
        to_edit3 = ("1234", "price", "70")
        to_edit4 = ("1235", "title", "Chocolate")
        to_edit5 = ("impossible", "impossible", "impossible")

        self.test_lst.edit(*to_edit1)
        self.assertEqual(getattr(TestLstCollection.Product_D, to_edit1[1]), to_edit1[2], "Edit method works improperly")
        self.test_lst.edit(*to_edit2)
        self.assertEqual(getattr(TestLstCollection.Product_D, to_edit2[1]), to_edit2[2], "Edit method works improperly")
        self.test_lst.edit(*to_edit3)
        self.assertEqual(getattr(TestLstCollection.Product_A, to_edit3[1]), to_edit3[2], "Edit method works improperly")
        self.test_lst.edit(*to_edit4)
        self.assertEqual(getattr(TestLstCollection.Product_B, to_edit4[1]), to_edit4[2], "Edit method works improperly")

        self.assertRaises(NameError, self.test_lst.edit, *to_edit5)

    def testUndo(self):
        self.assertRaises(AttributeError, self.caretaker.undo)
        self.test_lst.append(self.test_lst[0])
        self.caretaker.backup("Add new element.")

        self.caretaker.undo()
        self.assertListEqual([str(i) for i in self.test_lst], [str(i) for i in self.data],
                             "Undo method works improperly")

    def testRedo(self):
        self.assertRaises(AttributeError, self.caretaker.redo)
        self.test_lst.append(self.test_lst[0])
        self.data.append(self.test_lst[0])
        self.caretaker.backup("Add new element.")

        self.caretaker.undo()
        self.caretaker.redo()
        self.assertListEqual([str(i) for i in self.test_lst], [str(i) for i in self.data],
                             "Redo method works improperly")

    def testMove(self):
        self.assertRaises(AttributeError, self.caretaker.move_on_moment, 4)
        self.test_lst.append(self.test_lst[0])
        self.caretaker.backup("Add new element.")

        self.caretaker.move_on_moment(1)
        self.assertListEqual([str(i) for i in self.test_lst], [str(i) for i in self.data],
                             "Undo method works improperly")

    def test_read_json_file(self):
        self.assertRaises(ValueError, self.test_lst.read_json_file, "wrong_file_name")

        self.test_empty_lst.read_json_file("test_data.json")
        self.assertEqual(len(self.test_empty_lst), 3, "Read_json_file method works improperly")

        self.test_empty_lst.read_json_file("test_data.json")
        self.assertNotEqual(len(self.test_empty_lst), 3, "Read_json_file method works improperly")

        self.test_empty_lst.lst.clear()

    def test_write_json_file(self):
        self.assertRaises(ValueError, self.test_lst.read_json_file, "wrong_file_name")

        self.test_lst.write_in_json_file('test.json')
        self.test_empty_lst.read_json_file('test.json')
        self.assertEqual(len(self.test_empty_lst), 4)

        os.remove("test.json")


if __name__ == '__main__':
    unittest.main()
