class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self):
        return f"Book('{self.title}' by {self.author})"

    def is_long(self):
        return self.pages > 300

b1 = Book("Atomic Habits", "James Clear", 320)
b2 = Book("Python Course", "Eric", 200)

print(b1)
print(b1.is_long())
print(b2.is_long())

