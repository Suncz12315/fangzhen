import matplotlib.pyplot as plt
from scipy import integrate
import numpy as np
import sys
from function import *
from algorithm import *
import scipy.io as sio
#多无人机找寻路径
def process(total_num,coor):
    #各节点坐标及序号
    nodes = {}
    for i in range(0,total_num):
        nodes[i] = coor[i]
    dis = np.zeros((total_num,total_num),dtype = float)
    for i in range(0,total_num):
        for j in range(0,total_num):
            if i!=j:
                dis[i][j] = distance(nodes[i],nodes[j])
            else:
                #dis[i][j] = sys.float_info.max
                dis[i][j] = 0
    return nodes,dis

UAV = []
x = [] #节点数目
y_fh = [] #飞行时间
y_h = []
UAV_coor = [1700,2400]
UAV.append(data_center)
UAV.append(UAV_coor)
#coor = np.random.randint(500,4000,(total_num-2,2))
#################################################################
for node_num in range(1,15):
    total_num = node_num+2
    print("total_num = {}".format(total_num))
    coor = np.random.randint(500,4000,(total_num,2));
    for i in coor:
        UAV.append(i)
    E = np.random.rand(total_num)*1.5 #各节点能量
    B = np.random.rand(total_num)*10**7 #各节点信息量
    nodes,dis = process(total_num,UAV)


    t_hmin = np.zeros((total_num,total_num),dtype = float)
    t_min = np.zeros((total_num,total_num),dtype = float)
    h_min = hover_time(dis,t_hmin,total_num,E,B)
    #print(h_min)
    
    f_min = fly_time(dis,t_min,total_num,E,B)
    op_min = fly_hover(h_min,f_min,total_num)

    t_h = dp(h_min)
    t_fh = dp(op_min)
    x.append(node_num)
    y_h.append(t_h.time)
    y_fh.append(t_fh.time)
plt.figure(1)
plt.axis([0,15,0,500])
plt.xlabel('The number of sensor nodes N ')
plt.ylabel('The flight time of all nodes T(s)')
label = ['hover','fly_hover']
plt.plot(x,y_h,'b*')
plt.plot(x,y_fh,'ro')
plt.legend(label,loc = 2)
plt.show()

