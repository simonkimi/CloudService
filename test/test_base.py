import random

data = [{"a": random.randint(0, 100)} for _ in range(100)]


print(sorted(data, key=lambda x: x["a"]))
