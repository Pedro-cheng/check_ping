import os
from tools import get_time
import re

# List all the files in the address_book dir and make a valid choice
def chose_address_book():
    #list the files in the address_book dir
    valid_choice = None
    while valid_choice is None:
        try:
            print("List of address books:")
            all_files = os.listdir("address_book")
            for i, file in enumerate(all_files):
                # for human readability, start from 1
                print(f"{i+1:>3}{'':2}{file}")
            choice = input("Choose an address book (number or name): \n")
            # check if the input is a filename
            if choice in all_files:
                # choice is already a file name
                valid_choice = choice
                break
            # no available filename, check if the input is a number 
            else: 
                # added 1 former, so subtract 1 to get the index
                choice = int(choice) - 1
                if choice < 0 or choice > len(all_files):
                    raise ValueError
                # get filename
                valid_choice = all_files[choice]
        # not a valid filename and not a valid number
        except ValueError:
            print("Invalid choice")
    return os.path.join(os.path.curdir,'address_book',valid_choice)

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
            line_express = re.findall(r'[\d]{1,3}[\-]?[\d]{0,3}\.[\d]{1,3}[\-]?[\d]{0,3}\.[\d]{1,3}[\-]?[\d]{0,3}\.[\d]{1,3}[\-]?[\d]{0,3}',line)
            if line_express:
                for express in line_express:
                    yield(express)
    # remind to deal with StopIteration
    except StopIteration:
       pass 

# turn express generator into a address generator
def address_generator(express_generator):
    try:
        while True:
            # get next express
            express = next(express_generator)
            # 192-0.123.888.9-3 -> [('192', '0', '123', '', '888', '', '9', '3')]
            deal_express = re.findall(r'([\d]{1,3})[\-]?([\d]{1,3})?\.([\d]{1,3})[\-]?([\d]{0,3})?\.([\d]{1,3})[\-]?([\d]{0,3})?\.([\d]{1,3})[\-]?([\d]{0,3})?',express)
            ip_expression = deal_express[0]
            # todo : turn ip expression into a group address 
            ip = ip_expression
            yield ip
    # remind to deal with StopIteration
    except StopIteration:
        pass

if __name__ == "__main__":
    
    file = get_time(chose_address_book)
    line_generator = get_time(line_generator,file)
    express_generater = get_time(express_generator,line_generator)
    try:
        for i in range(17):
            print(get_time(next,address_generator(express_generater)))
    except StopIteration:
        print("No more addresses")