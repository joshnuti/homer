class ListOfModels(list):
    def __init__(self, iterable):
        super().__init__(item for item in iterable)

    def max_id(self):
        if len(self) == 0:
            return 0

        return max(self, key=lambda x: x.id).id

    def max_order(self):
        if len(self) == 0:
            return 0

        return max(self, key=lambda x: x.order).order

    def sort(self):
        sorted_list = sorted(self, key=lambda x: (x.order, x.name))
        self.clear()
        self.extend(sorted_list)

    def assign_missing_ids(self):
        if len(self) == 0:
            return

        missing_ids = list(filter(lambda x: x.id == None, self))

        if len(missing_ids) == 0:
            return

        if len(missing_ids) == len(self):
            max_id = 1
        else:
            has_ids = list(filter(lambda x: x.id != None, self))
            max_id = self.max_id()

        for elem in missing_ids:
            elem.id = max_id
            max_id += 1

    def assign_missing_order(self):
        if len(self) == 0:
            return

        missing_order = list(filter(lambda x: x.order == None, self))

        if len(missing_order) != len(self):
            return

        order = 1
        for elem in self:
            elem.order = order
            order += 1

    def clean(self):
        self.assign_missing_ids()
        self.assign_missing_order()
        self.sort()