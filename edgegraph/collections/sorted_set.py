"""
Sorted Set Implementation
"""

from typing import TypeVar, Sequence, Iterable

T = TypeVar("T")


class SortedSet(set[T], Sequence[T]):
    """
    Basic implementation of a set that maintains
    insertion order. Contents are accessible by index while
    preserving all set operations.
    """

    __slots__ = ("list",)

    def __init__(self, iterable: Iterable[T] | None = None):
        if isinstance(iterable, Iterable):
            self.list = list(iterable)
            super().__init__(self.list)
        elif iterable is None:
            super().__init__()
            self.list = []
        else:
            raise ValueError(f"Unable to initalize {self.__class__} from value")

    def add(self, element):
        if element not in self:
            self.list.append(element)
            super().add(element)

    def clear(self):
        self.list.clear()
        super().clear()

    def discard(self, element):
        if element in self:
            self.list.remove(element)
        super().discard(element)

    def remove(self, element):
        super().remove(element)
        self.list.remove(element)

    def _combine_lists(self, *s: Iterable[T]) -> list[T]:
        """
        Creates a copy of the current object's list and
        then extends it with data from other iterables

        :return: The extended list
        """

        comb_list = self.list.copy()
        for i in s:
            comb_list.extend(i)
        return comb_list

    def _rebuild_list(self, set_: set[T], *s: Iterable[T]) -> list[T]:
        """
        Filters an extended list to only include one of each key.
        The only the first instance of each key within the
        extended list will be preserved in the rebuild.

        :param set_: A consumable set of keys
        :return: The filtered list
        """
        comb_list = self._combine_lists(*s)
        new_list = []
        for j in comb_list:
            if j in set_:
                new_list.append(j)
                set_.remove(j)

        return new_list

    def difference(self, *s):
        new_set = super().difference(*s)
        return self.__class__(self._rebuild_list(new_set, *s))

    def difference_update(self, *s):
        super().difference_update(*s)
        self.list[:] = list(filter(lambda x: x in self, self.list))

    def intersection(self, *s):
        new_set = super().intersection(*s)
        return self.__class__(self._rebuild_list(new_set, *s))

    def intersection_update(self, *s):
        super().intersection_update(*s)
        self.list[:] = list(filter(lambda x: x in self, self.list))

    def symmetric_difference(self, s):
        new_set = super().symmetric_difference(s)
        comb_list = self._combine_lists(s)
        return self.__class__(filter(lambda x: x in new_set, comb_list))

    def symmetric_difference_update(self, s):
        super().symmetric_difference_update(s)
        comb_list = self._combine_lists(s)
        self.list[:] = list(filter(lambda x: x in self, comb_list))

    def union(self, *s):
        new_set = super().union(*s)
        comb_list = self._rebuild_list(new_set, *s)
        return self.__class__(comb_list)

    def update(self, *s):
        super().update(*s)
        self.list[:] = self._rebuild_list(super().copy(), *s)

    def pop(self, index: int = -1):
        i = self.list.pop(index)
        super().remove(i)
        return i

    def copy(self):
        return self.__class__(self.list)

    def __iter__(self):
        return self.list.__iter__()

    def __reversed__(self):
        return self.list.__reversed__()

    def __getitem__(self, index):
        return self.list.__getitem__(index)

    def __sub__(self, value):
        return self.difference(value)

    def __isub__(self, value):
        self.difference_update(value)
        return self

    def __and__(self, value):
        return self.intersection(value)

    def __iand__(self, value):
        self.intersection_update(value)
        return self

    def __or__(self, value):
        return self.union(value)

    def __ior__(self, value):
        self.update(value)
        return self

    def __xor__(self, value):
        return self.symmetric_difference(value)

    def __ixor__(self, value):
        self.symmetric_difference_update(value)
        return self

    def __repr__(self):
        vals = [f"{key}" for key in self.list]
        return f"{{{', '.join(vals)}}}"
