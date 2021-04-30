import sys
import time
from threading import Thread, Lock

mutex = Lock()

queue = {}

output = {}

counter = 0

def print_output(itr, name, curr, prev):
    print()
    print("For Iteration: {} ,Router table of {} ".format(itr, name))
    print()
    print("---------------------------------------")
    print(" Name        cost        Modified")
    print("----------------------------------------")
    for c in range(no_of_routers):
        nm = router_names[c]
        cst = curr[c]
        modified = " "
        if prev[c] != curr[c]:
            modified = "*"
        print(" {}          {}             {} ".format(nm, cst, modified))



def Bellman_Ford(router_table,neighbours,neighbour_tables,num):
    for i in range(no_of_routers):
        if i != num:
            final_cst = router_table[i]
            count = 0
            for nb in neighbours:
                table = neighbour_tables[count]
                val = neighbours[nb] + table[i]
                final_cst = min(val, final_cst)
                count = count + 1

            router_table[i] = final_cst
    return router_table


def target_thread(name, num):
    router_table = []
    i = 0
    #print(no_of_routers)
    for i in range(no_of_routers):
        router_table.append(999999)      # 999999 here  for infinity
    neighbours = graph[name]
    router_table[num] = 0
    for i in neighbours:
        indx = router_index[i]
        cst = neighbours[i]
        router_table[indx] = cst
    output[name] = list(router_table)
    z = []
    for m in range(len(router_table)):
        z.append(router_table[m])
        if z[m] == 999999:
            z[m] = "INF"
    print("{}             {}             {}".format("Initial", name, z))
    for itr in range(4):
        mutex.acquire()
        queue[name] = router_table.copy()
        mutex.release()
        f = 1
        while f:
            if len(queue) == no_of_routers:
                f = 0
        neighbour_tables = []
        for i in neighbours:
            neighbour_tables.append(queue[i])
        router_table = list(Bellman_Ford(router_table, neighbours, neighbour_tables, num))
        global counter
        mutex.acquire()
        counter = counter + 1
        mutex.release()
        f = 1
        while f:
            if counter == (itr+1) * no_of_routers:
                f = 0
        x = router_table.copy()
        for y in range(len(x)):
            if x[y] == 999999:
                x[y] = "-1"
        mutex.acquire()
        queue[name] = router_table.copy()
        last = list(output[name])
        output[name] = list(router_table.copy())
        print_output(itr+1, name, x, last)
        mutex.release()
        time.sleep(2)
        #print(output)
        #print()
        #print()
        """
        if itr in output:
            p = output[itr]
            p[name] = router_table
        else:
            p = {}
            p[name] = router_table
            output[itr] = p """




print("Enter the file name of input: ", end="")
f_name = input()
file = open(f_name, "r")
data = file.readlines()
line1 = data[0]
a = line1.split()
no_of_routers = int(a[0])
#print(no_of_routers)
router_names = []
router_index = {}
line2 = data[1]
router_names = line2.split()
for k in range(no_of_routers):
    router_index[router_names[k]] = k
#print(router_index)
k = 2
graph = {}
while data[k] != "EOF":
    line = data[k]
    word = line.split(" ")
    src = word[0]
    dest = word[1]
    cost = int(word[2])
    if src in graph:
        dct = graph[src]
        dct[dest] = cost
        if dest in graph:
            temp = graph[dest]
            temp[src] = cost
        else:
            temp = {}
            temp[src] = cost
            graph[dest] = temp
    else:
        dct = {}
        dct[dest] = cost
        graph[src] = dct
        if dest in graph:
            temp = graph[dest]
            temp[src] = cost
        else:
            temp = {}
            temp[src] = cost
            graph[dest] = temp
    k = k + 1

for j in router_names:
    if j not in graph:
        graph[j] = {}

print("-----------------------------------------------------------------")
print("Iteration          Name          Router-Table ")
print("-----------------------------------------------------------------")

threads = []

for j in range(no_of_routers):
    name = router_names[j]
    t = Thread(target=target_thread, args=(name, j))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

#print_output()

