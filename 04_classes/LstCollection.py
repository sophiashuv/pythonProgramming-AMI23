from Validation import Validation
from Product import Product
import uuid
import json


class LstCollection:
    """ Class for Collection on list representation."""

    def __init__(self, *lst):
        self.lst = list(lst[:])

    def __str__(self):
        return [str(el) for el in self.lst]

    def __getitem__(self, item):
        return self.lst[item]

    def __len__(self):
        return len(self.lst)

    def __setitem__(self, key, value):
        self.lst[key] = value

    def append(self, el):
        self.lst.append(el)

    def sort(self, field="title"):
        self.lst = sorted(self.lst, key=lambda product: str(getattr(product, field)).lower())

    def search(self, elem):
        filter_iter = list(filter(lambda x: any(elem in str(s) for s in x.__dict__.values()), self.lst))
        return filter_iter

    def delete(self, ID):
        for p in self.lst:
            if str(p.u_id) == ID:
                self.lst.remove(p)
                break
        else:
            raise NameError('No product with such ID found')

    def edit(self, ID, attr, val):
        for p in self.lst:
            if str(p.u_id) == ID:
                setattr(p, attr, val)

    def read_json_file(self, file_name):
        Validation.validateFileName(file_name, "json")
        f = open(file_name, encoding='utf-8')
        file = json.load(f)
        for i, product in enumerate(file):
            try:
                product["u_id"] = str(uuid.uuid4())
                self.lst.append(Product(**product))
            except ValueError as e:
                print("Line" + str(i * (len(product) + 1) + 3) + ": " + str(e))
                continue
        f.close()

    def write_in_json_file(self, file_name):
        Validation.validateFileName(file_name, "json")
        with open(file_name, 'w', encoding='utf-8') as outfile:
            json.dump([ob.__dict__ for ob in self.lst], outfile, ensure_ascii=False)
        outfile.close()

    def write_in_file(self, file_name, mode="w"):
        Validation.validateFileName(file_name)
        f = open(file_name, mode=mode, encoding="utf-8")
        f.writelines(str(i) + "\n" for i in self.lst)
        f.close()

    @staticmethod
    def add_el_to_file(file_name, element):
        Validation.validateFileName(file_name)
        f = open(file_name, mode="a", encoding="utf-8")
        f.write(str(element))
        f.close()