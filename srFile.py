import argparse, socket, time, sys, os
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mode", help="Set mode s/r send or receive", required=True)
parser.add_argument("-t", "--target", help="Set connection target ip")
parser.add_argument("-p", "--port", help="Set connection target port", required=True)
parser.add_argument("-f", "--file", help="Set file to send")

args = parser. parse_args()

if args.mode == 's' and args.file == None:
    raise Exception("[-] Unspecified file !")
if args.mode == "r" and args.file != None:
    args.file = None
if args.mode == "r" and args.target != None:
    args.target = None


if args.mode.lower() not in ['s', 'r']:
    raise Exception("[-] Unvalid mode !")



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if args.mode == 'r':
    sock.bind(('', int(args.port)))
    sock.listen(1)

    while 1:
        print("\n[+] Waiting connection on %s ... " % (args.port))
        conn, addr = sock.accept()
        ip, port = addr
        print("\n[+] Connection from %s:%s" %(ip, port))
        info = conn.recv(1024).decode()
        if os.path.exists(info):
            try:
                filename, extension = info.split('.')
                extension = "." + extension
            except:
                filename = info
                extension = ""
                pass
            date = datetime.now()
            filename += "_" + str(date.date()) + str(date.time()) + extension
            info = filename
        file = open(info, "wb")
        time.sleep(1)
        print("\n[+] Getting file  : ", info)
        data = conn.recv(1024)

        while data:
            file.write(data)
            data = conn.recv(1024)
        file.close()
        conn.close()
        break

if args.mode == 's':
    try:
        file = open(args.file, "rb")
    except FileNotFoundError:
        print("\n[-] Error with a file !\n")
        sys.exit(1)
    data = file.read(1024)

    sock.connect((args.target, int(args.port) ))
    sock.send(args.file.split(os.path.sep)[-1].encode())
    time.sleep(1)
    while data:
        sock.send(data)
        data = file.read(1024)
    file.close()
    sock.close()
