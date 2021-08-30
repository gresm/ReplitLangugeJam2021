class BiDirectionalListEmpty:
    pass


class BiDirectionalListElement:

    def __init__(self, value=None, before=None, after=None):
        super().__init__()
        self.value = value if value is not None else BiDirectionalListEmpty
        self.before = before
        self.after = after

    def __str__(self):
        if self.value is BiDirectionalListElement:
            return "BiDirectionalListElement(None, None, None)"
        return f"BiDirectionalListElement({self.value}, {self._str_b()}, {self._str_a()})"

    def __repr__(self):
        return str(self)

    def _str_b(self):
        return str(self.before.value) if self.before else "None"

    def _str_a(self):
        return str(self.after.value) if self.after else "None"


class BiDirectionalList:

    def __init__(self, *elements):
        super().__init__()

        self.length = len(elements)

        before = None
        first = None
        for value in elements:
            before2 = before
            before = BiDirectionalListElement(value, before)
            if before and before2:
                before.before = before2
                before2.after = before

            if not first:
                first = before

        if not first and not before:
            first = BiDirectionalListElement()
            before = first

        self.first = first
        self.last = before

    def empty(self):
        self.first = BiDirectionalListElement()
        self.last = self.first
        self.length = 0

    def pop_all(self):
        ret = list(self)
        self.empty()
        return ret

    def push_last(self, value):
        part = BiDirectionalListElement(value, self.last)
        if part.before:
            part.before.after = part
        self.last = part

        if self.first.value == BiDirectionalListEmpty:
            self.first = self.last
            self.last.before = None
        self.length += 1

    def push_all_from_last(self, values):
        for value in values:
            self.push_last(value)

    def pop_last(self):
        part = self.last
        if part.value == BiDirectionalListEmpty:
            raise IndexError("End of stack")
        else:
            self.length -= 1
        self.last = part.before if part.before else BiDirectionalListElement()
        self.last.after = None
        return part.value

    def push_first(self, value):
        part = BiDirectionalListElement(value, after=self.first)
        if part.after:
            part.after.before = part
        self.first = part

        if self.last.value == BiDirectionalListEmpty:
            self.last = self.first
            self.first.after = None

        self.length += 1

    def push_all_from_first(self, values):
        for value in values:
            self.push_first(value)

    def pop_first(self):
        part = self.first
        if part.value == BiDirectionalListEmpty:
            raise IndexError("End of stack")
        else:
            self.length -= 1
        self.first = part.after if part.after else BiDirectionalListElement()
        self.first.before = None
        return part.value

    def from_first(self):
        return BiDirectionalListValuesIter(self.first)

    def from_last(self):
        return BiDirectionalListValuesIter(self.last, True)

    def raw_from_first(self):
        return BiDirectionalListElementIter(self.first)

    def raw_from_last(self):
        return BiDirectionalListElementIter(self.last, True)

    def __iter__(self):
        return self.from_first()

    def __repr__(self):
        elements = list(self)
        shorted = []
        for el in elements:
            if el == BiDirectionalListEmpty:
                break
            shorted.append(repr(el))
        return f"<BiDirectionalList({', '.join(shorted)})>"

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        self.length = len(list(iter(self)))
        return self.length

    def __contains__(self, item):
        return item in set(self)


class BiDirectionalListElementIter:

    def __init__(self, stack, reverse=False):
        self.stack = stack
        self.reverse = reverse
        self.current = stack

    def __iter__(self):
        return self

    def __next__(self):
        current = self.current

        if not current:
            raise StopIteration

        if self.reverse:
            next_element = self.current.before
        else:
            next_element = self.current.after

        self.current = next_element
        return current


class BiDirectionalListValuesIter:

    def __init__(self, stack, reverse=False):
        self._iter = BiDirectionalListElementIter(stack, reverse)

    def __iter__(self):
        return self

    def __next__(self):
        return self._iter.__next__().value
