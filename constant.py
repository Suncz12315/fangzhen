import builtins as glb

#设置仿真参数
glb.W = 20000 # 带宽
glb.H = 100  # UAV高度
glb.v_max = 40.0 # UAV最大速度
glb.alpha = 2  # 路径损耗指数
glb.err = 10 # 误差指数
glb.sigma = 10**(-16) #噪声功率
glb.c = 3*10**8 #光速
glb.fc = 2*10**9 #载波频率
glb.beta = 0.14  #urban environment
glb.Gama = 11.95
glb.yita_1 = 2 #此处为3dB
glb.yita_2 = 199.5 #23dB

class result:
   def __init__(self):
        self.path = []
        self.time = 0
        
