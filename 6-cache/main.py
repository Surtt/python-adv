from typing import TypeVar, Generic, Optional

K = TypeVar("K")
V = TypeVar("V")


class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._store: dict[K, V] = {}

    def set(self, key: K, value: V) -> None:
        self._store[key] = value

    def get(self, key: K) -> Optional[V]:
        return self._store.get(key)

    def keys(self) -> list[K]:
        return list(self._store.keys())

    def values(self) -> list[V]:
        return list(self._store.values())


hits = Cache[str, int]()
hits.set("home", 10)
hits.set("about", 3)
x = hits.get("home")
paths = hits.keys()
counts = hits.values()
print(x)
print(paths)
print(counts)

# hits.set("contacts", "5")
# hits.get(123)
