import glob
import os
import os
import shutil
import time
import socket
import subprocess
import sys
from multiprocessing.connection import Listener
from multiprocessing.connection import Client


def get_last_file_by_pattern(pattern=None):
    files = glob.glob(pattern)
    if not files:
        return None
    if files:
        files.sort(key=os.path.getmtime)
        return files[-1]


def remove_dir(dir):
    try:
        shutil.rmtree(dir)
    except:
        sys.stderr.write("remove_dir: dir not found "+ dir +"\n")
        return


def gethostname():
    return socket.gethostname()

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s (%r) function took %0.3f ms' % (f.func_name,  args, (time2-time1)*1000.0)
        return ret
    return wrap

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result
    return timed

def build_work_dir():
    p = subprocess.Popen('mktemp -d', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    work_dir=p.stdout.readline().rstrip()
    return work_dir


def get_directory(path):
    return os.path.dirname(path)

def get_filename(path):
    return os.path.basename(path)

def wait_for_file(fn, msg, wait_time=5):
    while True:
        if not os.path.isfile(fn):
            print msg
            time.sleep(wait_time)
        else:
            return


def signal_listen(port):
    address = (gethostname(), port)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey='secret password')
    conn = listener.accept()
    #print 'connection accepted from', listener.last_accepted
    msg=conn.recv()
    return msg

def signal_send(host, port, msg='database loaded'):
    address = (host, port)     # family is deduced to be 'AF_INET'
    conn = Client(address, authkey='secret password')
    conn.send(msg)
    conn.close()



def get_new_port():
    s = socket.socket()
    host = '10.102.254.241'
    rport =  39785
    s.connect((host, rport))
    port= s.recv(1024)
    s.close()
    return int(port)
