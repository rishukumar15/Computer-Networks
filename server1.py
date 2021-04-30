import socket           #import the socket library
import sys


def activate(host, prt):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a server socket

    s.bind(('', prt))           #an empty string in ip makes the server listen to requests coming from other computers on the network

    print("socket binded to %s" % (prt))

    # put the socket into listening mode
    s.listen(1)
    print("socket is listening")

    f = 0

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        if f == 1:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', prt))
            s.listen(1)
            f = 0

        # Establish connection with client.
        c, addr = s.accept()
        print('----------------------------------------------------------')
        print('Got connection from', addr)
        print('----------------------------------------------------------')

        s.close()

        # send a thank you message to the client.
        c.send('Thank you for connecting'.encode())


        while True:
            expr = c.recv(1024)
            reqq = expr.decode()
            try:
                if reqq != "quit":
                    print("getting request....")
                    print("client with socket {} sent message: {}".format(addr[1], expr.decode()))
                    ans = str(eval(expr)).encode('utf-8')
                    # ans = str(eval(expr))
                    print("Sending reply: ", ans.decode())
                    c.send(ans)  # evaluate the expression and send the output
                else:
                    f = 1
                    print("client {} requested termination : connection closed".format(addr[1]))
                    break
            except:
                err_msg = "The string sent is not correct."
                print("Sending reply: ", err_msg)
                data = err_msg.encode('utf-8')
                c.send(data)


        # Close the connection with the client
        #c.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s [hostname] [port_number] " % sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    activate(hostname, port)

