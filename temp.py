import imghdr
import asyncio

@asyncio.coroutine
def open_file(name):
    print("opening {}".format(name))
    return open(name, 'rb')

@asyncio.coroutine
def close_file(file):
    print("closing {}".format(file.name))
    file.close()

@asyncio.coroutine
def read_data(file, n):
    print("reading {}".format(file.name))
    return file.read()

@asyncio.coroutine
def get_image_size(fname, future):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    fhandle = yield from asyncio.async(open_file(fname))
    
    head = yield from asyncio.async(read_data(fhandle, 24))
    if len(head) != 24:
        future.set_result(None)
    if imghdr.what(fname) == 'png':
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            future.set_result(None)
        width, height = struct.unpack('>ii', head[16:24])
    elif imghdr.what(fname) == 'gif':
        width, height = struct.unpack('<HH', head[6:10])
    elif imghdr.what(fname) == 'jpeg':
        try:
            fhandle.seek(0) # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                fhandle.seek(size, 1)
                byte = yield from asyncio.async(read_data(fhandle, 1))
                while ord(byte) == 0xff:
                    byte = yield from asyncio.async(read_data(fhandle, 1))
                ftype = ord(byte)
                s = s = yield from asyncio.async(read_data(fhandle, 2))
                size = struct.unpack('>H', s)[0] - 2
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
            s = yield from asyncio.async(read_data(fhandle, 4))
            height, width = struct.unpack('>HH', fhandle.read(4))
        except Exception: #IGNORE:W0703
            future.set_result(None)
    else:
        future.set_result(None)

    future.set_result((width, height))
    yield from close_file(fhandle)

def process_input():
    text = sys.stdin.readline()
    i = text.strip()
    future = asyncio.Future()
    asyncio.async(get_image_size(i, future))
    future.add_done_callback(got_size)
        
print("Open a file?\n$ ", end="")
loop = asyncio.get_event_loop()
loop.add_reader(sys.stdin, process_input)
try:
    loop.run_forever()
finally:
    loop.close()
