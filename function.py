from scipy import integrate
import numpy as np
import constant
import sys


#计算UAV到采集点的距离
def dis_sd(s):
    dis = np.sqrt(s**2+H**2)
    #print(dis)
    return dis
#LoS信道概率
def P_LoS(s):
    P = 1/(1+Gama*np.exp((-beta)*(180/np.pi*np.arcsin(H/dis_sd(s))-Gama)))
    #print(P)
    return P
#信道
def H_chl(s):
    hs = 1/((P_LoS(s)*yita_1+(1-P_LoS(s))*yita_2)*(4*np.pi*fc/c*dis_sd(s))**alpha)
    return hs
#计算速度  存在sigma和En影响问题
def v_m(x,d,En):
    s = np.linspace(0,d-x,10000)
    tmp = integrate.quad(lambda s:(1/H_chl(s)),0,d-x)[0]
    #print(tmp)
    v =(d-x)*sigma/(En*H_chl(d-x))-(sigma/En)*tmp
    return v

#计算注水上限
def gamma_0(x,d,v,En):
    s = np.linspace(0,d-x,10000)
    tmp = integrate.quad(lambda s:(1/H_chl(s)),0,d-x)[0]
    gamma_0 = En*v/(d-x)+sigma/(d-x)*tmp
    return gamma_0

#飞行模式计算B  随v单调递减
def fomu_B(x,d,v,En):
    gamma = gamma_0(x,d,v,En)
    s = np.linspace(0,d-x,10000)
    tmp = integrate.quad(lambda s:np.log2(gamma*H_chl(s)/sigma),0,d-x)[0]
    B = W/(2*v)*tmp
    #print("B={}".format(B))
    return B

#悬停模式计算B 随t单调递增
def B_hover(t,En):
    B = W/2*t*np.log2(1+En*H_chl(0)/(t*sigma))
    return B
#print(fomu_B(1000,2000,25,5))

#悬停模式寻找最优的t
def find_t(t_min,t_max,Bn,En):
    t_l = t_min
    t_r = t_max
    while t_l<t_r:
        t_mid = t_l+(t_r-t_l)/2
        B_max = B_hover(t_mid,En)
        if abs(B_max-Bn)<err:
            return t_mid
        elif B_max>Bn:
            t_r = t_mid
        else:
            t_l = t_mid

#飞行模式寻找最优的v
def find_v(v,v_max,Bn,x,d,En):
    v_l = v
    v_r = v_max
    #print("v_l:")
    #print(v_l)
    while v_l<v_r:
        v_mid = v_l+(v_r-v_l)/2
        B_max = fomu_B(x,d,v_mid,En)
        #print("B_max = {}".format(B_max))
        if abs(B_max - Bn)<err:
            return float(v_mid)
        elif B_max>Bn:
            v_l = v_mid
        else:
            v_r = v_mid

#计算坐标间距离
def distance(coor1,coor2):
    distance = np.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
    return distance

#计算悬停模式下的时间矩阵
def hover_time(dis,t_hmin,node_num,E,B):
    for i in range(0,node_num):
        for j in range(0,node_num):
            if(i!=j):
                t_hmin[i][j] = dis[i][j]/v_max
    for i in range(0,node_num):
        for j in range(1,node_num):
            t_cs = 100000
            B_max = B_hover(t_cs,E[j])
            if i!=j and B_max>B[j]:
                t_hmin[i][j] +=find_t(0,t_cs,B[j],E[j])
            else:
                t_hmin[i][j] = 0
    for i in range(0,node_num):
        if i != 1:
            t_hmin[0][i] = sys.float_info.max
    return t_hmin

#计算飞行模式下的时间矩阵
def fly_time(dis,t_min,node_num,E,B):
    for i in range(0,node_num):
        for j in range(1,node_num):
            if i!=j:
                t_min_m = sys.float_info.max
                for x in range(1,int(dis[i][j]),10):
                    d = dis[i][j]
                    En = E[j]
                    v_min = v_m(x,d,En)
                    #print(v_min)
                    B_max = fomu_B(x,d,v_min,En)
                    if B_max>B[j] and v_min<v_max:
                       # print(B[j])
                        v_opt = find_v(v_min,v_max,B[j],x,d,En)
                        #print(v_opt)
                        #print(B_max)
                        if(v_opt and v_opt>5.0):#当UAV速度小于5时，不采用飞行模式
                            t_op = (d-x)/v_opt+x/v_max
                            t_min_m = min(t_min_m,t_op)
                t_min[i][j] = t_min_m
     for i in range(0,node_num):
        if i != 1:
            t_min[0][i] = sys.float_info.max
    return t_min
#飞行悬停模式时间矩阵           
def fly_hover(t_hmin,t_min,node_num):
    for i in range(0,node_num):
        for j in range(1,node_num):
            if t_min[i][j]>t_hmin[i][j]:
                t_min[i][j] = t_hmin[i][j]
    return t_min
