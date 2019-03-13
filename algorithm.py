from constant import result
import numpy as np
import constant
import sys
import random
#贪心算法
def greedy(t):
    size = len(t)
    res = result()
    visited = [True]*size
    visited[0] = False
    res.path = [0]*size
    count = 1
    record = 0
    while count<size:
        min_t = sys.float_info.max
        for row in range(0,size):
            if visited[row]:
                min_t = min(t[record][row],min_t)
        for i in range(0,size):
            if visited[i] and min_t==t[record][i]:
                visited[i] = False
                res.path[count] = i
        res.time+=min_t
        record = res.path[count]
        count = count+1
    res.time+=t[res.path[count-1]][0]
    res.path.append(0)
    #print(res.path)
    return res

#动态规划算法
def dp(t):
    size = len(t)
    res = result()
    bit_set = 1<<(size-1)
    #print(bit_set)
    #dp = [list() for i in range(0,bit_set)]
    #pos = [list() for i in range(0,bit_set)]
    dp = np.zeros((size,bit_set))
    pos = np.ones((size,bit_set),dtype = int)
    for i in range(0,size):
        dp[i][0] = t[i][0]
    for j in range(1,bit_set):
        for i in range(0,size):
            dp[i][j] = sys.float_info.max
            if i-1>=0 and ((j>>(i-1))&1)==1:
                continue
            for k in range(1,size):
                if ((j>>(k-1))&1)==0:
                    continue
                if dp[i][j]>t[i][k]+dp[k][j^(1<<(k-1))]:
                    dp[i][j]=t[i][k]+dp[k][j^(1<<(k-1))]
                    #print(dp[i][j])
                    pos[i][j] = k
    res.path.append(0)
    idx = bit_set-1
    m = 0
    while idx>0:
        #print(pos[m][i])
        m = pos[m][idx]
        idx = idx-(1<<m-1)
        res.path.append(m)
        
    res.path.append(0)
    #print(res.path)
    res.time = dp[0][bit_set-1]
    return res


#模拟退火算法
T_init = 5000
T_temi = 1e-8
delta = 0.98
limit = 1000
outloop = 2000
inloop = 6000

#求某一路径和
def get_sum(t,path):
    size = len(t)
    #print(size)
    sum_t = 0.0
    record = 0
    #print(path)
    for j in range(1,size+1):
        sum_t+=t[record][path[j]]
        record = path[j]
   # print("sum_t = {}".format(sum_t))
    return sum_t

#获取下一路径
def get_nxt(path,t):
    res = result()
    size = len(path)-2
    x = 0
    y = 0
    #print("idx")
    while x==y:
        x = random.randint(1,size)
        y = random.randint(1,size)
        #print("x = {0},y = {1}".format(x,y))
    temp = path
    #print("temp ={} ".format(temp))
    temp[x],temp[y] = temp[y],temp[x]
    #print("temp = {}".format(temp))
    res.time = get_sum(t,temp)
    res.path = temp
    return res

def annealing(t):
    size = len(t)
    res = result()
    curpath = result()
    newpath = result()
    curpath = greedy(t)
    newpath = curpath
    path = curpath.path
    sum_t = curpath.time
    P_L = 0
    P_F = 0
    t_ini = T_init
    while True:
        for i in range(0,inloop):
            newpath = get_nxt(path,t)
            #print("newpath = {}".format(newpath.time))
            dE = newpath.time-curpath.time
            if dE<0:
                curpath = newpath
                P_L = 0
                P_F = 0
            else:
                rd = random.random()
                e = np.exp(-dE/t_ini)
                if e>rd and e<1:
                    curpath = newpath
                P_L+=1
                if P_L>limit:
                    P_F+=1
                    break
        if curpath.time<sum_t:
            path = curpath.path
            #print(path)
            sum_t = curpath.time
            #print("sum_t = {}".format(sum_t))
        if P_F>outloop or t_ini<T_temi:
            break
        t_ini*=delta
    #print(path)
    res.time = sum_t
    res.path = path
    return res

    
