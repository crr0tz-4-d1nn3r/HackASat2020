'''
Here is the output from a CCD Camera from a star tracker, identify as many 
stars as you can! (in image reference coordinates) Note: The camera prints 
pixels in the following order (x,y): (0,0), (1,0), (2,0)... (0,1), (1,1), (2,1)…
Note that top left corner is (0,0)
'''
from telnetlib import Telnet
from time import sleep

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm


# connection info
host = 'stars.satellitesabove.me'
port = 5013
ticket = b'ticket{victor86037juliet:GMcb2fTUEzOhZDfm5k3o1ZzTKWfLRq2jzucHXKKInSQaw9UoQ_d1pUtBIymaplqyDg}\r\n'

# connect
tn = Telnet(host, port)
sleep(1)

# ticket info
r = tn.read_very_eager().decode('ascii')
print(r)
tn.write(ticket)
sleep(3)
r = tn.read_very_eager().decode('ascii')
print(r)

ans = [[15,44],[18,73],[41,53],[43,81],[80,49],[83,25],[97,85],[103,114],[119,59], [119,95]]
for a in ans:
    msg = str(a[0]) + ',' + str(a[1]) + '\n'
    print(msg)
    tn.write(msg.encode('ascii'))

tn.write(b'\n')
sleep(1)
r = tn.read_very_eager().decode('ascii')
print(r)


ans=[[23,92],[43,19],[43,108],[46,52],[61,89],[66,73],[74,113],[92,29],[99,110],[118,72]]
for a in ans:
    msg = str(a[0]) + ',' + str(a[1]) + '\n'
    print(msg)
    tn.write(msg.encode('ascii'))

tn.write(b'\n')
sleep(1)
r = tn.read_very_eager().decode('ascii')
print(r)


ans = [[24,26],[28,102],[39,63],[47,85],[70,8],[75,62],[85,91],[99,18],[121,92],[121,120]]
for a in ans:
    msg = str(a[0]) + ',' + str(a[1]) + '\n'
    print(msg)
    tn.write(msg.encode('ascii'))

tn.write(b'\n')
sleep(1)
r = tn.read_very_eager().decode('ascii')
print(r)

ans = [[13,5],[17,32],[20,84],[40,70],[44,27],[60,43],[61,16],[96,88],[102,115],[113,28]]
for a in ans:
    msg = str(a[0]) + ',' + str(a[1]) + '\n'
    print(msg)
    tn.write(msg.encode('ascii'))

tn.write(b'\n')
sleep(1)
r = tn.read_very_eager().decode('ascii')
print(r)

ans = [[8,68],[43,51],[43,71],[69,60],[72,10],[73,95],[87,53],[102,109],[107,37],[119,102]]
for a in ans:
    msg = str(a[0]) + ',' + str(a[1]) + '\n'
    print(msg)
    tn.write(msg.encode('ascii'))

tn.write(b'\n')
sleep(1)
r = tn.read_very_eager().decode('ascii')
print(r)

'''
lines = r.splitlines()
arr = []
for line in lines:
    if line == '':
        break
    a = line.split(',')
    if len(a) < 10:
        continue
    oMap = map(int,a)
    arr.append(list(oMap))
    

plt.imsave('stars.png', np.array(arr).reshape(len(arr[0]),len(arr)), cmap=cm.gray)

t1 = []
for a in arr:
    t1.append([x < 138 for x in a])

plt.imsave('stars_t1.png', np.array(t1).reshape(len(t1[0]),len(t1)), cmap=cm.gray)

for i in range(len(t1)-1):
    for j in range(len(t1[i])-1):
        if not t1[i][j]:
                msg = str(i) + ',' + str(j) + '\n'
                print(msg)
                tn.write(msg.encode('ascii'))


ans = [[15,44],[18,73],[41,53],[43,81],[80,49],[83,25],[97,85],[103,114],[119,59], [119,95]]
for a in ans:
    msg = str(a[0]) + ',' + str(a[1]) + '\n'
    print(msg)
    tn.write(msg.encode('ascii'))


'''

tn.write(b'\n')
sleep(1)
r = tn.read_very_eager().decode('ascii')
print(r)
