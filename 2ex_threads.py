from threading import Thread
from time import sleep
from time import time
import sys
from functools import wraps


def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        return_value = func(*args, **kwargs)
        message = "\nExecuting {} took {:.03} seconds.\n$ ".format(func.__name__,
                                                             time() - start)
        print(message, end="")
        return return_value
    return wrapper
	
	
def fib(n):
    return fib(n - 1) + fib(n - 2) if n > 1 else n


timed_fib = log_execution_time(fib)


def print_hello():
    while True:
        print("\nI am a thread of Jordi doing a loong coffee!\n$ ", end="")
        sleep(5)

def read_and_process_input():
    while True:
        i = input()
        if i == 'quit' or i == 'exit': 
            sys.exit(0)
        n = int(i)
        print("\nAnother thread of Jordi calculating fib...\n$ ", end="")
        print('\nended: fib({}) = {}\n$ '.format(n, timed_fib(n)), end="")


def main():
    print("input a large number (30) to get fibonacci result or exit to get kickout")
    # Second thread will print the hello message. Starting as a daemon means
    # the thread will not prevent the process from exiting.
    t = Thread(target=print_hello)
    t.daemon = True
    t.start()
    # Main thread will read and process input
    read_and_process_input()

if __name__ == '__main__':
    main()