from scipy import integrate
import scipy.io as sio
import numpy as np
load_fn ='pos.mat'
load_data = sio.loadmat(load_fn)
coor = load_data['data']
#print(load_data)
relate = 'relate.mat'
data = sio.loadmat(relate)
rel = data['x']
#rel = np.array(rel)
size = len(rel)
UAV = [list() for i in range(3)]
for i in range(0,size):
    #rel[i].sort()
   # print(len(rel[i]))
    for j in range(0,len(rel[i])):
        if rel[i][j]>0.9:
            #print(coor[j])
            #print(rel[i][j])
            UAV[i].append(list(coor[j]))
            

#print(rel)
#print(coor)
print(UAV)
#print(type(load_data))

