import random
import socket
import string
import sys
import threading
import time


thread_num = 0
thread_num_mutex = threading.Lock()


def print_status():
    global thread_num
    thread_num_mutex.acquire(True)
    thread_num += 1
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] Hold your tears")
    sys.stdout.flush()
    thread_num_mutex.release()


def attack(ip, port):
    print_status()
    
    # create socket
    http_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    	# open connection
        #insert your code
        
        
        # forge http request
        # insert your code
        
        
        # send http request
		# insert your code      
       
       
    except socket.error:
        print("No connection")
        
    finally:
        http_conn.shutdown(socket.SHUT_RDWR)
        http_conn.close()


def main():
    ip = input("Enter target IP: ")
    num_requests = input("Enter threads (you can leave this blank): ")
    try:
        ip = socket.gethostbyname(ip)
        num_requests = 1000 if num_requests == '' else int(num_requests)
        
    except:
        sys.exit(1)
    all_threads = []
    
    for i in range(num_requests):
    
        t = threading.Thread(target=attack, args=(ip, 80))
        t.deamon=True
        t.start()
        all_threads.append(t)
        time.sleep(0.01)
        
    for t in all_threads:
        t.join()


if __name__ == "__main__":
    main()
