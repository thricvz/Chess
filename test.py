class Parent:
    name = "bugs all over the place"
    def __init__(self):
        self.nme = "hey"

class Child(Parent):
    def __init__(self):
        self.papa = super().__init__()

    def change_name(self):
       print(Parent.name)
       print(self.papa.nme)
        

a = Parent()
b = Child()
print(a.name)
b.change_name()
print(a.name)