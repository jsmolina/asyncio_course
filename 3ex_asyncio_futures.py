import asyncio
import time
import sys

breakfast_status = {
    'coffee': False,
    'milk': False
}

@asyncio.coroutine
def microwave(future):
    print('Microwave starts\n$ ', end="")
    yield from asyncio.sleep(5)
    future.set_result('\nGot milk!')


def got_milk(future):
    breakfast_status['milk'] = True
    print(future.result()+ "\n$ ", end="")
    
@asyncio.coroutine
def coffee(future2):
    print('The coffee machine will take 20 secs\n$ ', end="")
    
    start = time.time()
    while time.time() - start < 20:
        yield from asyncio.sleep(2)
    future2.set_result('Got coffee!')

def got_coffee(future):
    breakfast_status['coffee'] = True
    print("\n" + future.result() + "\n$ ", end="")

def process_input():
    text = sys.stdin.readline()
    i = text.strip()
    if i == 'milk':
        future = asyncio.Future()
        asyncio.async(microwave(future)) #asyncio.ensure_future(slow_operation(future))
        future.add_done_callback(got_milk)
    elif i == 'coffee':
        future2 = asyncio.Future()
        asyncio.async(coffee(future2)) #asyncio.ensure_future(slow_operation(future))
        future2.add_done_callback(got_coffee)
    elif i == 'quit' or i == 'exit':
        print("See'ya next time")
        loop.stop()
    elif i == "breakfast":
        if breakfast_status['milk'] and breakfast_status['coffee']:
            print("Nyam!! bye!")
            loop.stop()
        else: 
            print("you should prepare it first!\n$ ", end="")
    else:
        if i != "":
            print("Sorry, can you repeat?")
        

print("I woke up really asleep, coffee and milk? breakfast when done\n$ ", end="")
loop = asyncio.get_event_loop()




loop.add_reader(sys.stdin, process_input)
try:
    loop.run_forever()
finally:
    loop.close()