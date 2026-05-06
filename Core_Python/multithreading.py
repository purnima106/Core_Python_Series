#Multithreading is a technique where multiple threads run concurrently within the same process to improve performance, especially for I/O-bound tasks.

import threading

def print_numbers():
    for i in range(5):
        print(i)

t1 = threading.Thread(target = print_numbers)
t2 = threading.Thread(target = print_numbers)

t1.start()
t2.start()

t1.join()
t2.join()