#Multithreading is a technique where multiple threads run concurrently within the same process to improve performance, especially for I/O-bound tasks.

# import threading

# def print_numbers():
#     for i in range(5):
#         print(i)

# t1 = threading.Thread(target = print_numbers)
# t2 = threading.Thread(target = print_numbers)

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# import time

# def task():
#     print("Start")
#     time.sleep(2)
#     print("End")

# task()
# task()

#Race Condition
#Race condition occurs when multiple threads access shared resources concurrently,
#and the outcome depends on the unpredictable order in which threads execute.
#To avoid race conditions, use locks to synchronize access to shared resources.

# import threading

# counter = 0

# def increment():
#     global counter
#     for _ in range(5):
#         counter += 1
#         print(counter)

# t1 = threading.Thread(target=increment)
# t2 = threading.Thread(target=increment)

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# print("Final Counter:", counter)

import threading
import time

counter = 0

def increment():
    global counter
    for _ in range(5):
        temp = counter
        time.sleep(0.1)
        temp += 1
        counter = temp
        print(counter)

t1 = threading.Thread(target = increment)
t2 = threading.Thread(target = increment)

t1.start()
t2.start()

t1.join()
t2.join()

print("Final Counter:", counter)



