import time

def timer(func):#function and another func
    def wrapper(*args, **kwargs):#inner func
        start = time.time() 
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[timer] {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def train_model(epochs): #Define function with parameter epochs
    time.sleep(0.5)#Pause for 0.5 seconds (simulate work)
    print(f"Model trained for {epochs} epochs")

train_model(10)

