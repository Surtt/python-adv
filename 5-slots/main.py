import sys


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class SlotUser:
    __slots__ = ("name", "email", "password")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


N = 100_000

users = [User(f"user_{i}", f"u{i}@mail.com", f"p{i}") for i in range(N)]
slot_users = [SlotUser(f"user_{i}", f"u{i}@mail.com", f"p{i}") for i in range(N)]

u_size = sys.getsizeof(users[0]) + sys.getsizeof(users[0].__dict__)
s_size = sys.getsizeof(slot_users[0])

print(f"User:     {u_size} байт/объект → {u_size * N / 1024 / 1024:.1f} МБ")
print(f"SlotUser: {s_size} байт/объект → {s_size * N / 1024 / 1024:.1f} МБ")
print(f"Экономия: ~{(1 - s_size / u_size) * 100:.0f}%")
