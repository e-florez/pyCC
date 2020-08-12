#!/usr/bin/python3.8


import matplotlib.pyplot as plt
import sys

print (sys.argv)

exit()

f = open(os.path.expanduser("a.txt"))
lines = f.readlines()

x, y = [], []

for line in lines:
    x.append(line.split()[0])
    y.append(line.split()[1])

f.close()

print(x, y)

plt.plot(x,y)
plt.show()
