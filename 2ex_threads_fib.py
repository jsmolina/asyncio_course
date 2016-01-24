from threading import Thread, Lock, BoundedSemaphore
from time import sleep
from time import time
import sys
from functools import wraps


import time

pool_outputs = []
lock = Lock()

def fib(number):
    a, b = 0, 1
    for i in range(number):
        a, b = b, a + b
    return a

def execute_fib(n):
   o = fib(n)
   # do the lock to avoid collide
   lock.acquire()
   pool_outputs.append(o)
   lock.release() 

def execute_semaphored_threads():
    inputs = list(range(800, 1000))
    print("Calculating from {} to {}".format(inputs[0], inputs[-1]))
    # only four threads at time
    pool_sema = BoundedSemaphore(value=4)
    threads = []
    for i in inputs:
        # limit threads amount
        pool_sema.acquire()
        t = Thread(target=execute_fib, args=(i,))
        threads.append(t)
        t.start()
        pool_sema.release()
    return threads
        
    
if __name__ == '__main__':
    start = time.time()
    threads = execute_semaphored_threads()
    # wait for all threads
    for t in threads:
        t.join()

    print('Len of outputs:', len(pool_outputs))
    print('Done in {} seconds' .format(time.time() - start))
    print('I am faster, but I need to worry about shared memories')