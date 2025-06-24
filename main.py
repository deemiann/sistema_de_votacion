class UnsortedTableMap:
    class _Item():
        def __init__(self, k, v):
            self._key = k
            self._value = v

    def __init__(self):
        self._table = []

    def __getitem__(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError("Key Error: " + repr(k))

    def __setitem__(self, k, v):
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v))
    
    def __delitem__(self, k):
        for i in range(len(self._table)):
            if i == self._table[i]._key:
                del self._table[i]
                return
        raise KeyError("Key Error: " + repr(k))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key

    def items(self):
        for item in self._table:
            yield item._key, item._value

    def __str__(self):
        s = []
        for item in self._table:
            s += f"{item._key}: {item._value}"
        return "{" + ", ".join(f"\'{k}\': {v}" for k, v in self.items()) + "}"

class HashMapBase:
    def __init__(self):
        self._table = 11 * [None]

    def _hash_function(self, k):
        return sum(ord(c) for c in k) % 11

    def __setitem__(self, k, v):
        i = self._hash_function(k)
        if self._table[i] is None:
            self._table[i] = UnsortedTableMap()
        self._table[i][k] = v
        return v

    def __getitem__(self, k):
        i = self._hash_function(k)
        if self._table[i] != None:
            return self._table[i][k]
        return None

    def __iter__(self):
        for bucket in self._table:
            yield bucket

vot = HashMapBase()
vot["24022424"] = 24
for i in vot:
    print(i)
print("-"*24)
persona = UnsortedTableMap()
persona["name"] = "demian"
persona["age"] = 18
vot["24022433"] = persona
for i in vot:
    print(i)
