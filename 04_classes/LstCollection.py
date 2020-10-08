from Validation import Validation
from Product import Product
import uuid


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

    def read_file(self, file_name):
        Validation.validateTxtFileName(file_name)
        f = open(file_name, "r")
        for i, line in enumerate(f):
            try:
                line = list(line.split(", "))
                u_id = uuid.uuid4()
                # line.append(str(u_id))
                # k = [i for i in Product.__dict__.keys() if not i.startswith('__')
                #     and not i.startswith('_') and i != "input_product"]
                # k.append("description").append("u_id")
                # print(len(k), len(line))
                # kk = dict(zip(k, line))
                # print(kk)
                # p = Product(**kk)
                title, image_url, price, created_at, updated_at, description = line
                self.lst.append(Product(title=title, image_url=image_url, price=price, created_at=created_at,
                                        updated_at=updated_at, description=description, u_id=u_id))
                # self.lst.append(p)
            except ValueError as e:
                print("Line" + str(i+1) + ": " + str(e))
                continue
        f.close()

    def write_in_file(self, file_name, mode="w"):
        Validation.validateTxtFileName(file_name)
        f = open(file_name, mode=mode, encoding="utf-8")
        f.writelines(str(i) + "\n" for i in self.lst)
        f.close()

    @staticmethod
    def add_el_to_file(file_name, element):
        Validation.validateTxtFileName(file_name)
        f = open(file_name, mode="a", encoding="utf-8")
        f.write(str(element))
        f.close()