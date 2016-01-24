import asyncio
import time
import sys
from concurrent.futures import ProcessPoolExecutor

pool_outputs = []

@asyncio.coroutine
def fib(number):
    a, b = 0, 1
    for i in range(number):
        yield from asyncio.sleep(0)
        a, b = b, a + b
    return a

@asyncio.coroutine    
def execute_fib(n):
   o = yield from fib(n)  
   pool_outputs.append(o)
   return 

                         
if __name__ == '__main__':
    inputs = list(range(800, 1000))
    print("Calculating from {} to {}".format(inputs[0], inputs[-1]))
    
    loop = asyncio.get_event_loop()
    
    start = time.time()
    tasks = [asyncio.async(execute_fib(i)) for i in inputs]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    print('Len of outputs:', len(pool_outputs))
    print('Done in {} seconds' .format(time.time() - start))
    print('I am a bit slower, but no one worried for semaphores, locks or whatever')