import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.timer()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[timer] {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

