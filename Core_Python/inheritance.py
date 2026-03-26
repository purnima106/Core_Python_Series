class Animal: #classvariable
    species_count = 0 #this will be shared among all onjects

    def __init__(self, name, sound): #constructor
        self.name = name #these 2 are instance variables
        self.sound = sound
        Animal.species_count += 1 #count increases everytime and object is created

    def __repr__(self) -> str: #defines how object is printed
        return f"Animal('{self.name}')"
    
    def speak(self):
        return f"{self.name} says {self.sound}"

    @classmethod
    def how_many(cls):
        return f"Total animals created: {cls.species_count}"

    @staticmethod
    def is_wild(habitat):
        return habitat in ["jungle", "ocean", "forest"]

class Dog(Animal):
        def __init__(self, name, breed):
            super().__init__(name, sound="Woof")
            self.breed = breed
        
        def __repr__(self):
            return f"Dog('{self.name}', breed ='{self.breed}')"

        def speak(self):
            return f"{self.name} barks loudly: {self.sound}!!"
        
class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, sound="Meow")
        self.indoor = indoor

    def speak(self):
        mood = "softly" if self.indoor else "loudly"
        return f"{self.name} meows {mood}"

d = Dog("Bub", "Lab") 
c = Cat("Whisk", indoor=False)

print(d)
print(d.speak())
print(c.speak())

print(Animal.how_many())          # classmethod
print(Animal.is_wild("jungle"))   # staticmethod
print(Animal.is_wild("apartment"))
        
