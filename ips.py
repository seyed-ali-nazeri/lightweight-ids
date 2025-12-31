import subprocess, os, signal

def block_ip(ip):
    try:
        subprocess.run(
            ["iptables", "-A", "OUTPUT", "-d", ip, "-j", "DROP"],
            check=True
        )
        return True
    except:
        return False

def kill_process(pid):
    try:
        os.kill(pid, signal.SIGKILL)
        return True
    except:
        return False
