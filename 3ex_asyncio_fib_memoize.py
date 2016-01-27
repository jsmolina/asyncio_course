import asyncio
import time
import sys
from concurrent.futures import ProcessPoolExecutor

pool_outputs = []

caches = {}

@asyncio.coroutine
def fib(n):
    # avoid recursive
    if n in caches:
        return caches[n]

    if n < 2:
        return n

    v1 = yield from fib(n-2)
    v2 = yield from fib(n-1)
    caches[n] = v1 + v2
    return v1 + v2


@asyncio.coroutine    
def execute_fib(n):
   o = yield from fib(n)  
   pool_outputs.append(o)
   return 

                         
if __name__ == '__main__':
    inputs = list(range(800, 1000))
    print("Calculating from {} to {}".format(inputs[0], inputs[-1]))
    print("note: it is not recommended do a calculus like this in asyncio")
    print("but I can do a simple memoize without worrying for locks")
    
    loop = asyncio.get_event_loop()
    
    start = time.time()
    tasks = [asyncio.async(execute_fib(i)) for i in inputs]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    print('Len of outputs:', len(pool_outputs))
    print('Done in {} seconds' .format(time.time() - start))
    print('I can memoize, no worries for locks!')
