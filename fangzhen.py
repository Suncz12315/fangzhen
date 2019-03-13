import matplotlib.pyplot as plt
from scipy import integrate
import numpy as np
import sys
from function import *
from algorithm import *
import scipy.io as sio
#多无人机找寻路径
def process(node_num,coor):
    #各节点坐标及序号
    nodes = {}
    for i in range(0,node_num):
        nodes[i] = coor[i]
        dis = np.zeros((node_num,node_num),dtype = float)
    for i in range(0,node_num):
        for j in range(0,node_num):
            if i!=j:
                dis[i][j] = distance(nodes[i],nodes[j])
            else:
                dis[i][j] = sys.float_info.max
                #dis[i][j] = 0
    return nodes,dis

########################得到各无人机及关联用户坐标###############
#获得节点位置矩阵
load_fn ='pos.mat'
load_data = sio.loadmat(load_fn)
coor = load_data['data']
#获得节点关联矩阵
relate = 'relate.mat'
data = sio.loadmat(relate)
rel = data['x']
size = len(rel)
#给定UAV坐标
UAV_coor = [[1700,2400],[2200,2600],[2500,3200]]
UAV = [list() for i in range(0,size)]
for i in range(0,size):
    UAV[i].append(UAV_coor[i])
    for j in range(0,len(rel[i])):
        if rel[i][j]>0.9:
            UAV[i].append(list(coor[j]))
##################################################################
save = [list() for i in range(0,len(UAV))]
for k in range(0,len(UAV)):
    node_num = len(UAV[k])
    E = np.random.rand(node_num)*1.5 #各节点能量
    B = np.random.rand(node_num)*10**7 #各节点信息量
    nodes,dis = process(node_num,UAV[k])
            

#coor = np.random.randint(500,4000,(node_num,2))


    t_hmin = np.zeros((node_num,node_num),dtype = float)
    t_min = np.zeros((node_num,node_num),dtype = float)
    h_min = hover_time(dis,t_hmin,node_num,E,B)
    print(h_min)
    #f_min = fly_time(dis,t_min,node_num,E,B)
    #op_min = fly_hover(h_min,f_min,node_num)
    '''
    t_hover = greedy(h_min)
    t_fh = dp(h_min)
    print(t_hover.time)
    print(t_hover.path)
    print(t_fh.time)
    print(t_fh.path)
    '''
    
'''
    city = []
    x = []
    y = []
    #画路径图
    for i in t_fh.path:
        city.append(i)
        x.append(nodes[i][0])
        y.append(nodes[i][1])
    save[k].append(x)
    save[k].append(y)
    save[k].append(city)

plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.axis([1000,3500,500,4000])
line1, = plt.plot(save[0][0],save[0][1],'bo-',label = 'UAV_1')
plt.annotate('UAV_1', xy=(save[0][0][0], save[0][1][0]), xytext=(1500, 1500),arrowprops=dict(facecolor='black', width = 0.1,headwidth = 5))
line2, = plt.plot(save[1][0],save[1][1],'r^-',label = 'UAV_2')
plt.annotate('UAV_2', xy=(save[1][0][0], save[1][1][0]), xytext=(2200, 1500),arrowprops=dict(facecolor='black', width = 0.1,headwidth = 5))
line3, = plt.plot(save[2][0],save[2][1],'g*-',label = 'UAV_3')
plt.annotate('UAV_3', xy=(save[2][0][0], save[2][1][0]), xytext=(3000, 3000),arrowprops=dict(facecolor='black', width = 0.1,headwidth = 5))

plt.legend([line1,line2,line3],['UAV_1','UAV_2','UAV_3'] ,loc = 2)
plt.show()
'''
