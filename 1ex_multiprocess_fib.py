import multiprocessing
import time

def fib(number):
    a, b = 0, 1
    for i in range(number):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    inputs = list(range(800, 1000))
    print("Calculating from {} to {}".format(inputs[0], inputs[-1]))
    start = time.time()
    pool = multiprocessing.Pool(processes=4)
    # This method chops the iterable into a number of chunks 
    # which it submits to the process pool as separate tasks.
    # It blocks until the result is ready    
    pool_outputs = pool.map(fib, inputs)
    # Indicate that no more data will be put on this queue by the current process
    pool.close()
    # Wait for the worker processes to exit.
    pool.join()
    print('Len of outputs:', len(pool_outputs))
    print('Done in {} seconds' .format(time.time() - start))