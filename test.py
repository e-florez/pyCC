
import matplotlib.pyplot as plt

x, y = [], []
for line in open("O-H_rda.dat", 'r'):
   # skipping the header
   if line.startswith("#"):
       continue

   values = [float(s) for s in line.split()]
   x.append(values[0])
   y.append(values[1])

plt.plot(x, y, label='O-H_rda.dat')
plt.show()
