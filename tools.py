import time,os,re
import multiprocessing as mp

# warapper - count run time
def count_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

# get test time
@count_time
def get_time(func,*args):
    return func(*args)

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

def get_ports(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    # [ 'a', 'b', 'c', 'd']
    #print(content)
    ports = re.findall(r'\b[\d]{1,5}\b',content)
    return set(ports)

def get_report_path(filedir,localtime):
    filename = time.strftime('%Y-%m-%d-%H%M%S', localtime)
    dir_path = os.path.join(os.path.curdir,filedir)
    file_path = os.path.join(dir_path,filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return file_path
    
    

if __name__ == '__main__':
    print(get_ports('check_ports'))