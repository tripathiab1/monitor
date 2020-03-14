import threading

def init():
    global nthreads
    global lock
    global stop
    global condition
    nthreads = 0
    stop = False
    lock = threading.Lock()
    messages = []
    condition = threading.Condition()
