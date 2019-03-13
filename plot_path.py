import matplotlib.pyplot as plt
import re

def loadData(filename):
    myfile = open(filename,'r')

    city = []
    x = []
    y = []
    for line in myfile:
        data = line.split(',')
        city.append(data[0])
        x.append(data[1])
        y.append(data[2])
    return city,(x,y)
plt.figure(1)
city,(x,y) = loadData("greedy.txt")

plt.axis([0,4000,0,4000])
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.plot(x,y,'bo-')

for a, b, c in zip(x, y,city):  
    plt.text(a, b, c,ha='center', va='bottom', fontsize=15)
plt.annotate('the second node', xy=(x[1], y[1]), xytext=(1000, 2000),arrowprops=dict(facecolor='black', width = 0.1,headwidth = 5))
plt.legend(["the optimal path(greedy)"])
#plt.show()

plt.figure(2)
city,(x,y) = loadData("annealing.txt")

plt.axis([0,4000,0,4000])
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.plot(x,y,'bo-')

for a, b, c in zip(x, y,city):  
    plt.text(a, b, c,ha='center', va='bottom', fontsize=15)
plt.annotate('the second node', xy=(x[1], y[1]), xytext=(1000, 2000),arrowprops=dict(facecolor='black', width = 0.1,headwidth = 5))
plt.legend(["the optimal path(annealing)"])
plt.figure(3)
city,(x,y) = loadData("dp.txt")

plt.axis([0,4000,0,4000])
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.plot(x,y,'bo-')

for a, b, c in zip(x, y,city):  
    plt.text(a, b, c,ha='center', va='bottom', fontsize=15)
plt.annotate('the second node', xy=(x[1], y[1]), xytext=(1000, 2000),arrowprops=dict(facecolor='black', width = 0.1,headwidth = 5))
plt.legend(["the optimal path(dp)"])
plt.show()
