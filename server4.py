import socket           #import the socket library
import sys
import select

def activate(host, prt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a server socket

    sock.bind(('', prt))           #an empty string in ip makes the server listen to requests coming from other computers on the network

    print("socket binded to %s" % (prt))

    # put the socket into listening mode
    sock.listen(1)
    print("socket is listening")

    socket_list = [sock]        #list of sockets(only main server socket now)

    clients = {}  # list of client sockets, wherein client socket is key and the addr is value

    while True:
        read_socks, _, excep_socks = select.select(socket_list, [], socket_list)

        for s in read_socks:
            if s is sock:
                #some new connection initiated
                conn, addr = sock.accept()
                conn.setblocking(0)
                socket_list.append(conn)  # appending the new connection to all active connections
                clients[conn] = addr  # remembering clients
                print('----------------------------------------------------------')
                print('Got connection from', addr)
                print('----------------------------------------------------------')
                conn.send('Thank you for connecting'.encode())
            else:
                # some existing conn/sock sent a message
                try:
                    expr = s.recv(1024)
                    if not expr:
                        socket_list.remove(s)       #if the client terminates connection then remove it from active list
                        del clients[s]

                    reqq = str(expr.decode())
                    if reqq != "quit" and reqq != '':
                        print("getting request....")
                        temp = clients[s]
                        print("client with socket {} sent message: {}".format(temp[1], expr.decode()))
                        print("Sending reply: ", expr.decode())
                        s.sendall(expr)  # evaluate the expression and send the output
                    elif reqq == "quit":
                        print("client {} requested termination : connection closed".format(temp[1]))
                except:
                    socket_list.remove(s)       #if the client terminates connection then remove it from active list
                    del clients[s]









if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s [hostname] [port_number] " % sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    activate(hostname, port)