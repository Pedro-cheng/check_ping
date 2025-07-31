import subprocess, platform, socket
from tools import count_time

def ping_alive(host, timeout=1):
    count = "-n" if platform.system().lower() == "windows" else "-c"
    wait  = "-w" if platform.system().lower() == "windows" else "-W"
    timeout_ms = timeout*1000 if platform.system().lower() == "windows" else timeout
    cmd = ["ping", count, "1", wait, str(timeout_ms), host]
    return subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def tcp_alive(host, port=80, timeout=1):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, socket.timeout):
        return False

def check_alive(host:str, possible_ports:tuple):
    # ping_test failed
    if not ping_alive(host=host,timeout=1):
        for port in possible_ports:
            if tcp_alive(host=host,port=port,timeout=1):
                return True
        return False
    return True

# 测试
if __name__ =='__main__':
    test_ip = [
        ('119.29.29.29'),
        ('8.8.8.8'),
        ('114.114.114.114'),
        ('192.168.88.88')
        ]
    test_port = (53,80,443,8080,8443)
    @count_time
    def count_through():
        for address in test_ip:
            print(f'ping test {address:>16}{'':6} : {ping_alive(address)}')
            for ports in test_port:
                print(f'tcp test {address:>17}:{ports:<5} : {tcp_alive(address,ports)}')
    @count_time
    def count_skip():
        for address in test_ip:
            print(f"{address:>16} check: {check_alive(host=address,possible_ports=test_port)}")
        
    count_through()
    count_skip()