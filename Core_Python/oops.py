class Book: #(class(blueprint))
    def __init__(self, title, author, pages): #(this is constructor(__init__))
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self): #(Controls how object is printed)
        return f"Book('{self.title}' by {self.author})"

    def is_long(self): #(custom method-to check pages)
        return self.pages > 300

    def get_pages(self):
        return self.pages

#these are objects
b1 = Book("Atomic Habits", "James Clear", 320)
b2 = Book("Python Course", "Eric", 200)

print(b1) #for this __repr__is used
print(b1.is_long())
print(b2.is_long())
print(b1.pages)
print(b1.get_pages())



