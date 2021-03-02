class A:
    def __init__(self):
        self.data = 123



a = A()

a.__setattr__('data', 321)

print(a.data)

