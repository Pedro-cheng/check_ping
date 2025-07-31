import subprocess, platform, socket

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


# 测试
if __name__ =='__main__':
    test_set = [('8.8.8.8',(53,80,443)),('114.114.114.114',(53,80,443))]
    for host in test_set:
        address = host[0]
        print(f'ping test\t{address}\t\t: {ping_alive(address)}')
        for ports in host[1]:
            print(f'tcp test\t{address}:{ports}\t: {tcp_alive(address,ports)}')