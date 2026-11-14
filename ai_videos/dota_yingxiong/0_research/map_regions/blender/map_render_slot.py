"""Serialize memory-heavy whole-map jobs and reserve headroom for local generation."""
from contextlib import contextmanager
import ctypes,json,os,time
class MemoryStatus(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(name,ctypes.c_ulonglong) for name in ['total_physical','available_physical','total_page','available_page','total_virtual','available_virtual','available_extended']]
def memory_headroom():
    value=MemoryStatus();value.length=ctypes.sizeof(value)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(value)):raise ctypes.WinError()
    # ullAvailPageFile is additional commit available to this process, not
    # merely free page-file space. Physical RAM alone did not prevent v022 OOM.
    return {'physical':value.available_physical,'commit':value.available_page}

def available_memory():
    return memory_headroom()['physical']
def alive(pid):
    handle=ctypes.windll.kernel32.OpenProcess(0x1000,False,pid)
    if not handle:return False
    ctypes.windll.kernel32.CloseHandle(handle);return True
@contextmanager
def map_render_slot(folder,minimum_gib=64,timeout=3*3600,minimum_commit_gib=None):
    minimum_commit_gib=minimum_gib if minimum_commit_gib is None else minimum_commit_gib
    path=folder/'map_render_slot.lock';deadline=time.monotonic()+timeout;owned=False;last_notice=0
    while time.monotonic()<deadline:
        if path.exists():
            try:
                owner=json.loads(path.read_text(encoding='utf-8'))
                if not alive(owner['pid']):path.unlink();continue
            except (json.JSONDecodeError,FileNotFoundError):pass
            time.sleep(5);continue
        memory=memory_headroom()
        if memory['physical']<minimum_gib*1024**3 or memory['commit']<minimum_commit_gib*1024**3:
            if time.monotonic()-last_notice>60:
                print('WAIT_MAP_MEMORY',json.dumps({'physical_gib':round(memory['physical']/1024**3,2),'commit_gib':round(memory['commit']/1024**3,2),'required_physical_gib':minimum_gib,'required_commit_gib':minimum_commit_gib}),flush=True);last_notice=time.monotonic()
            time.sleep(10);continue
        try:
            with path.open('x',encoding='utf-8') as stream:json.dump({'pid':os.getpid(),'at':time.time()},stream)
            owned=True;break
        except FileExistsError:continue
    if not owned:raise TimeoutError('Whole-map render slot or memory headroom unavailable')
    try:yield
    finally:
        if path.exists() and json.loads(path.read_text())['pid']==os.getpid():path.unlink()
