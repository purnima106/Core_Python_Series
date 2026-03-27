# class Animal: #Base Class
#     species_count = 0 #this will be shared among all onjects (#classvariable)

#     def __init__(self, name, sound): #constructor
#         self.name = name #these 2 are instance variables
#         self.sound = sound
#         Animal.species_count += 1 #count increases everytime and object is created

#     def __repr__(self) -> str: #defines how object is printed
#         return f"Animal('{self.name}')"
    
#     def speak(self): #instance method #workds on individual object
#         return f"{self.name} says {self.sound}"

#     @classmethod
#     def how_many(cls): #cls refers to class, here we wilaccess class variable
#         return f"Total animals created: {cls.species_count}"

#     @staticmethod #utility function inside class
#     def is_wild(habitat):
#         return habitat in ["jungle", "ocean", "forest"]

# class Dog(Animal): #childclass inherits everything from Animal
#         def __init__(self, name, breed):
#             super().__init__(name, sound="Woof") #super-Calls parent (Animal) constructor
#             self.breed = breed #breed will be extra property
        
#         def __repr__(self):
#             return f"Dog('{self.name}', breed ='{self.breed}')"

#         def speak(self):
#             return f"{self.name} barks loudly: {self.sound}!!"
        
# class Cat(Animal):
#     def __init__(self, name, indoor=True):
#         super().__init__(name, sound="Meow")
#         self.indoor = indoor

#     def speak(self):
#         mood = "softly" if self.indoor else "loudly"
#         return f"{self.name} meows {mood}"

# d = Dog("Bub", "Lab")  #these two are objects
# c = Cat("Whisk", indoor=False)

# print(d)
# print(d.speak())
# print(c.speak())

# print(Animal.how_many())          # classmethod
# print(Animal.is_wild("jungle"))   # staticmethod
# print(Animal.is_wild("apartment"))

class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def move(self):
        return f"{self.brand} moves at {self.speed} km/hr"

class Car(Vehicle):
        def __init__(self, brand,speed,fuel_type):
            super().__init__(brand,speed)
            self.fuel_type = fuel_type

        def  move(self):
            return f"{self.brand} car drives on road at {self.speed} km/h"

class Bike(Vehicle):
    def __init__(self, brand, speed, type):
         super().__init__(brand, speed)
         self.type = type

# creating objects
c = Car("Tesla", 120, "Electric")
b = Bike("Yamaha", 80, "Sports")

print(c.move())
print(b.move())


