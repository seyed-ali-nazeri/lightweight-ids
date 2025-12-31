import os, time, psutil, logging, hashlib
from config import *
from ips import block_ip, kill_process
from report import add_event, generate_report

logging.basicConfig(
    filename="/var/log/ids.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log(level, msg):
    print(msg)
    getattr(logging, level.lower())(msg)
    add_event(level, msg)

def sha256(path):
    try:
        h = hashlib.sha256()
        with open(path,"rb") as f:
            h.update(f.read(2048))
        return h.hexdigest()
    except:
        return None

def get_files():
    data={}
    for r,_,fs in os.walk(WATCH_PATH):
        for f in fs:
            p=os.path.join(r,f)
            try:
                data[p]=os.path.getsize(p)
            except:
                pass
    return data

def get_ports():
    return {c.laddr.port for c in psutil.net_connections() if c.status=="LISTEN"}

def get_ips():
    return {c.raddr.ip for c in psutil.net_connections() if c.raddr}

def get_procs():
    out={}
    for p in psutil.process_iter(['pid','name']):
        try:
            cpu=p.cpu_percent(interval=0.1)
            out[p.pid]=(p.info['name'],cpu)
        except:
            pass
    return out

files_old=get_files()
ports_old=get_ports()
ips_old=get_ips()
procs_old=get_procs()

alerts=[]

try:
    while True:
        time.sleep(SLEEP_TIME)

        # FILE MONITOR
        files_new=get_files()
        for f in files_new:
            if f not in files_old:
                lvl="WARNING"
                if f.endswith(DANGER_EXT):
                    lvl="CRITICAL"
                log(lvl,f"[NEW FILE] {f} HASH:{sha256(f)}")
        files_old=files_new

        # PROCESS
        procs_new=get_procs()
        for pid,(name,cpu) in procs_new.items():
            if pid not in procs_old and name not in WHITELIST_PROCS:
                log("WARNING",f"[NEW PROCESS] {name}({pid}) CPU:{cpu}%")
            if cpu>CPU_SPIKE:
                log("CRITICAL",f"[CPU SPIKE] {name}({pid})")
                if ENABLE_IPS:
                    kill_process(pid)
                    log("CRITICAL",f"[IPS] Killed PID {pid}")
        procs_old=procs_new

        # PORT
        ports_new=get_ports()
        for p in ports_new-ports_old:
            if p not in WHITELIST_PORTS:
                log("WARNING",f"[NEW PORT] {p}")
        ports_old=ports_new

        # IP
        ips_new=get_ips()
        for ip in ips_new-ips_old:
            log("WARNING",f"[NEW IP] {ip}")
            if ENABLE_IPS:
                block_ip(ip)
                log("CRITICAL",f"[IPS] Blocked IP {ip}")
        ips_old=ips_new

except KeyboardInterrupt:
    generate_report()
    print("IDS stopped. Report generated.")
