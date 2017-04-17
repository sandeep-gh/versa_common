import glob
import os
import os
import shutil
import time
import socket
import subprocess
import sys
import xmlutils as xu
from multiprocessing.connection import Listener
from multiprocessing.connection import Client

module_dir=os.path.dirname(os.path.realpath(__file__))

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






system_config_xml_fn = None
import os.path
from  system_config import config_dir
if os.path.isfile(config_dir + '/dicex_haswell.sh'):
    system_config_xml_fn = module_dir + '/haswell_system_config.xml'
if os.path.isfile(config_dir+ '/dicex_shadowfax.sh'):
    system_config_xml_fn = module_dir + '/shadowfax_system_config.xml'

print "system_config_xml  = ", system_config_xml_fn
system_config_root = xu.read_file(system_config_xml_fn)
cluster_login_ip = xu.get_value_of_key(system_config_root, 'port_server_ip')
def get_new_port(port_server_ip=None):
    global cluster_login_ip
    if port_server_ip is None:
        port_server_ip = cluster_login_ip
    s = socket.socket()
    rport =  39785
    s.connect((port_server_ip, rport))
    port= s.recv(1024)
    print "recived port ", port
    s.close()
    return int(port)

def get_qsub_queue_args(host_type='standard'):
    cluster_name = xu.get_value_of_key(system_config_root, 'cluster_name')
    qsub_group_list=xu.get_value_of_key(system_config_root, 'cluster/job_queue/' + host_type + '/group')
    qsub_q=xu.get_value_of_key(system_config_root, 'cluster/job_queue/'+host_type+'/queue_name')
    return [qsub_group_list, qsub_q]
    


def get_port_server_ip():
    port_server_ip=xu.get_value_of_key(system_config_root, 'port_server_ip')
    return port_server_ip

def get_cluster_name():
    cluster_name = xu.get_value_of_key(system_config_root, 'cluster_name')
    return cluster_name

def get_dicex_base_dir():
    dicex_base_dir = xu.get_value_of_key(system_config_root, 'dicex_base_dir')
    return dicex_base_dir
