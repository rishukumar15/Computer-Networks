# Import socket module

import socket
import sys

def run(host, prt):
    cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server on local computer
    cl.connect((host, prt))

    print(cl.recv(1024).decode())

    while True:
        print("Please enter the message to the server or quit to exit: ", end='')
        req = input()

        if req == "quit":
            cl.send(req.encode("utf-8"))
            cl.close()
            print("connection closed")
            exit(0)
        else:
            print("Sending request....")
            cl.send(req.encode("utf-8"))
            ans = cl.recv(1024)
            print("Server replied: ", end='')
            print(ans.decode())






if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s [hostname] [port_number] " % sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    run(hostname, port)




