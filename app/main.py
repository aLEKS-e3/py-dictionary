from typing import Hashable, Any
from app.node import Node


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def _indexing(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for node in self.hash_table:
            if node:
                index = self._indexing(node.key)
                while new_table[index]:
                    index = (index + 1) % self.capacity
                new_table[index] = node

        self.hash_table = new_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._indexing(key)

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = Node(hash(key), key, value)
                self.length += 1
                break

            if (self.hash_table[index].key == key
                    and self.hash_table[index].hashed == hash(key)):
                self.hash_table[index].value = value
                break

            index = (index + 1) % self.capacity

        if self.length > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._indexing(key)
        current = self.hash_table[index]

        while current:
            if (current.key == key
                    and current.hashed == hash(current.key)):
                return current.value
            index = (index + 1) % self.capacity
            current = self.hash_table[index]
        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        index = self._indexing(key)

        while self.hash_table[index] and self.hash_table[index].key != key:
            index = (index + 1) % self.capacity

        self.hash_table[index] = None
        self.length -= 1

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Hashable) -> Any:
        value = self.__getitem__(key)
        self.__delitem__(key)
        return value

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def clear(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __iter__(self) -> iter:
        for node in self.hash_table:
            if node:
                yield node.key

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return f"{[node for node in self.hash_table if node]}"
