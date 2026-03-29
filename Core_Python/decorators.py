# def hello():
#     print("Hello, World!")
#     print("Hello, World!")
#     print("Hello, World!")

# hello()

#A decorator = wrap a function and add extra behavior

# def my_decorator(func):
#     def wrapper(*args, **kwargs):
#         print("Something is happening before the function is called.")
#         func(*args, **kwargs)
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_hello(name):
#     print("Hello, World!", name)

# say_hello("Purnima")

# def loud(func):
#     def wrapper(*args, **kwargs):
#         print("!!!")
#         func(*args, **kwargs)
#         print("!!!")
#     return wrapper

# @loud
# def saybye(name):
#     print("Bye!", name)

# saybye("Purnima")

import time
def timer(func):
    # wraps any function and prints how long it took
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[timer] {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def train_model(epochs):
    time.sleep(0.5)  # simulating training
    print(f"Model trained for {epochs} epochs")

train_model(10)

def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def log_status(msg):
    print(f"[log] {msg}")
log_status("Training started")

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return (self.celsius * 9/5) + 32

t = Temperature(25)

print(t.celsius)
print(t.fahrenheit)
t.celsius = 100
print(t.celsius)
print(t.fahrenheit)

class FileLogger:
    def __init__(self, filename):
        self.filename = filename


class FileLogger:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w")
        print(f"File {self.filename} opened")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        print(f"File {self.filename} closed")
        return False

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

t = Temperature(25)
print(t.celsius)      # calls getter
print(t.fahrenheit)   # computed on the fly
t.celsius = 100       # calls setter
print(t.fahrenheit)


# ─── Part 4: context manager ───────────────────────────────────────────────

class FileLogger:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w")
        print(f"[logger] opened {self.filename}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        print(f"[logger] closed {self.filename}")
        return False  # don't suppress exceptions

with FileLogger("output.log") as f:
    f.write("Training started\n")
    f.write("Epoch 1 complete\n")