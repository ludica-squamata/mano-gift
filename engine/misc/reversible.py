class ReversibleDict:
    """This object stores pairs of values. The object may be acceded by key, where the key
     is one of the values of a pair."""
    _left = None
    _right = None
    _lenght = None

    def __init__(self, **kwargs):
        self._left = []
        self._right = []
        self._lenght = 0
        for item in kwargs:
            self[item] = kwargs[item]

    def __getitem__(self, key):
        if key in self._left:
            idx = self._left.index(key)
            return self._right[idx]
        elif key in self._right:
            idx = self._right.index(key)
            return self._left[idx]

        elif type(key) is int:
            macro = self._left + self._right
            macro.sort()
            if 0 <= key <= len(macro) - 1:
                return macro[key]
            else:
                raise IndexError()
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if key in self._left:
            idx = self._left.index(key)
            self._left[idx] = key
            self._right[idx] = value
        else:
            self._left.append(key)
            self._right.append(value)
            self._lenght += 2

    def __delitem__(self, key):
        if key in self._left:
            idx = self._left.index(key)
        elif key in self._right:
            idx = self._left.index(key)
        else:
            raise IndexError()

        del self._left[idx]
        del self._right[idx]
        self._lenght -= 2

    def __contains__(self, key):
        if key in self._left or key in self._right:
            return True
        else:
            return False

    def __len__(self):
        return self._lenght

    def clear(self):
        """"Remove all items from the ReversibleDict"""
        self._left.clear()
        self._right.clear()
        self._lenght = 0

    def items(self):
        """Return a new view of the ReversibleDict items((key, value) pairs)."""
        macro = []
        for i in range(self.n_pairs()):
            macro.append((self._left[i], self._right[i]))
        return macro

    def n_pairs(self):
        """Return the number of pairs in the ReversibleDict"""
        return self._lenght // 2
