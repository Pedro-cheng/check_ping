import os
from tools import get_time,count_time,chose_address_book
import re


# generate lines from choosed file
def line_generator(address_book):
    print(f"Check the hosts in \"{address_book}\" !")
    with open(address_book, "r") as f:
        for line in f:
            # get rid of empty lines and comments
            if (not line.strip()) or line.strip().startswith("#"):
                pass
            else:
                yield line
# turn line generator into express generator
def express_generator(line_generator):
    try:
        while True:
            # get next line
            line = next(line_generator)
            # match ipv4 expression x(-y).x(-y).x(-y).x(-y) like 192.168.0.1-255
            line_express = re.findall(r'([\d]{1,3})[\-]?([\d]{1,3})?\.([\d]{1,3})[\-]?([\d]{0,3})?\.([\d]{1,3})[\-]?([\d]{0,3})?\.([\d]{1,3})[\-]?([\d]{0,3})?',line)
            #line_express = re.findall(r'[\d]{1,3}[\-]?[\d]{0,3}\.[\d]{1,3}[\-]?[\d]{0,3}\.[\d]{1,3}[\-]?[\d]{0,3}\.[\d]{1,3}[\-]?[\d]{0,3}',line)
            #print(line_express)
            if line_express:
                for express in line_express:
                    yield(express)
    # remind to deal with StopIteration
    except StopIteration:
       pass 

# turn express generator into a address generator
def address_generator(express_generator):
    def ip_sort(num1,num2):
        valid_num = set()
        for n in num1,num2:
            if len(n)>0:
                valid_num.add(min(max(0,int(n)),255))
        # range(n,n+1) = n
        return min(valid_num),max(valid_num)+1
    try:
        while True:
            # get next express like ('192', '0', '123', '', '888', '', '9', '3')
            a1,a2,b1,b2,c1,c2,d1,d2 = next(express_generator)
            # make a.b.c.d
            for a in range(*ip_sort(a1,a2)):
                for b in range(*ip_sort(b1,b2)):
                    for c in range(*ip_sort(c1,c2)):
                        for d in range(*ip_sort(d1,d2)):
                                yield f"{a}.{b}.{c}.{d}"
    # remind to deal with StopIteration
    except StopIteration:
        pass

def build_ip_pool(file):
    line_gener = line_generator(file)
    express_gener = express_generator(line_gener)
    address_gener = address_generator(express_gener)
    return address_gener


if __name__ == "__main__":
    
    file = get_time(chose_address_book)
    address_gener = get_time(build_ip_pool,file)
    @count_time
    def get_all_ip(address_generator):
        n = 0
        try:
            while(True):
                n += 1
                next(address_gener)
        except StopIteration:
            print(f"No more addresses, total address : {n}")
    get_all_ip(address_gener)