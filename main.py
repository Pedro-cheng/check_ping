import get_address,check_alive,tools
import multiprocessing as mp
import time

PORTS = tools.get_ports('check_ports')
IP_POOL = mp.Queue()
FAILED = mp.Queue()

def init_ip_pool(ip_generator):
    # get all ip into queue for multiprocessing
    try:
        for ip in ip_generator:
             IP_POOL.put(ip)
    except StopIteration:
        pass

def process_check_alive(ip_pool,output):
    try:
        while True:
            # ip_pool done
            if ip_pool.empty():
                break
            # get a new IP from pool
            host_ip = ip_pool.get()
            # check host alive
            is_alive = check_alive.check_alive(host_ip,PORTS)
            print(f"{host_ip:<18} : {is_alive}")
            if is_alive == False:
                output.put(host_ip)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    process_limit = 16
    input_file = tools.chose_address_book()
    ip_pool = init_ip_pool(get_address.build_ip_pool(input_file))
    processes = []
    try:
        num_process = 0
        while num_process < process_limit:
            p = mp.Process(target=process_check_alive,args=(IP_POOL,FAILED))
            p.start()
            processes.append(p)
            num_process += 1
    # up to 16
    except OSError:
        print(f"current run {num_process} processes")

    for p in processes:
        p.join()
    res = []
    while not FAILED.empty():
        res.append(FAILED.get())
    report_path = tools.get_report_path('fail_reports',time.localtime())
    with open(report_path,'a',encoding='utf-8') as f:
        print('\n'.join(res),file=f)
    print(f"all {len(res)} failed ip , report path : {report_path}")
