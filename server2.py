import socket           #import the socket library
import sys
from threading import Thread


def activate(host, prt):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a server socket

    s.bind(('', prt))           #an empty string in ip makes the server listen to requests coming from other computers on the network

    print("socket binded to %s" % (prt))

    # put the socket into listening mode
    s.listen(6)
    print("socket is listening")


    # a forever loop until we interrupt it or
    # an error occurs
    while True:

        # Establish connection with client.
        c, addr = s.accept()

        ip, pt = str(addr[0]), str(addr[1])
        Thread(target=client_thread, args=(c, ip, pt)).start()


def client_thread(conn, ip, pt):
    print('----------------------------------------------------------')
    print('Got connection from (', ip, ' ', pt, ')')
    print('----------------------------------------------------------')

    # send a thank you message to the client.
    conn.send('Thank you for connecting'.encode())

    while True:
        expr = conn.recv(1024)
        reqq = expr.decode()
        try:
            if reqq != "quit":
                print("getting request....")
                print("client with socket {} sent message: {}".format(pt, expr.decode()))
                ans = str(eval(expr)).encode('utf-8')
                # ans = str(eval(expr))
                print("Sending reply: ", ans.decode())
                conn.send(ans)  # evaluate the expression and send the output
            else:
                print("client {} requested termination : connection closed".format(pt))
                break
        except:
            err_msg = "The string sent is not correct."
            print("Sending reply: ", err_msg)
            data = err_msg.encode('utf-8')
            conn.send(data)




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s [hostname] [port_number] " % sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    activate(hostname, port)

