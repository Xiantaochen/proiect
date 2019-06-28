import math
capacity=1000000000
error_rate=0.00000001
m = math.ceil(capacity*math.log2(math.e)*math.log2(1/error_rate))      #需要的总bit位数
k = math.ceil(math.log1p(2)*m/capacity)                           #需要最少的hash次数
mem = math.ceil(m/8/1024/1024)
print(m)
print(mem)