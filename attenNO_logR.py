import math
import numpy as np

P5R2 = 10**(-2.7186 + 0.8330*5 + (0.7350 -0.1442* 5)*2)
P5R27 = 10**(-2.7186 + 0.8330*5 + (0.7350 -0.142* 5)*math.log10(500))
P5R3 = 10**(-2.7186 + 0.8330*5 + (0.7350 -0.1442* 5)*3)
P5R37 = 10**(-2.7186 + 0.8330*5 + (0.7350 -0.1442* 5)*math.log10(5000))
P5R4 = 10**(-2.7186 + 0.8330*5 + (0.7350 -0.1442* 5)*4)
 
print(np.round(P5R2,4))
print(np.round(P5R27,4))
print(np.round(P5R3,4))
print(np.round(P5R37,4))
print(np.round(P5R4,4))

print(np.round((P5R2-P5R27)/P5R2*100,4).real)
print(np.round((P5R27-P5R3)/P5R27*100,4))
print(np.round((P5R3-P5R37)/P5R3*100,4))
print(np.round((P5R37-P5R4)/P5R37*100,4))

print('%%%%%')
P6R2 = 10**(-2.7186 + 0.8330*6 + (0.7350 -0.1442* 6)*2)
P6R27 = 10**(-2.7186 + 0.8330*6 + (0.7350 -0.1442* 6)*math.log10(500))
P6R3 = 10**(-2.7186 + 0.8330*6 + (0.7350 -0.1442* 6)*3)
P6R37 = 10**(-2.7186 + 0.8330*6 + (0.7350 -0.1442* 6)*math.log10(5000))
P6R4 = 10**(-2.7186 + 0.8330*6 + (0.7350 -0.1442* 6)*4)
 
print(np.round(P6R2,4).real)
print(np.round(P6R27,4).real)
print(np.round(P6R3,4).real)
print(np.round(P6R37,4).real)
print(np.round(P6R4,4).real)


print(np.round((P6R2-P6R27)/P5R2*100,4).real)
print(np.round((P6R27-P6R3)/P5R27*100,4).real)
print(np.round((P6R3-P6R37)/P5R3*100,4).real)
print(np.round((P6R37-P6R4)/P5R37*100,4).real)
print('%%%%%')

P7R2 = 10**(-2.7186 + 0.8330*7 + (0.7350 -0.1442* 7)*2)
P7R27 = 10**(-2.7186 + 0.8330*7 + (0.7350 -0.1442* 7)*math.log10(500))
P7R3 = 10**(-2.7186 + 0.8330*7 + (0.7350 -0.1442* 7)*3)
P7R37 = 10**(-2.7186 + 0.8330*7 + (0.7350 -0.1442* 7)*math.log10(5000))
P7R4 = 10**(-2.7186 + 0.8330*7 + (0.7350 -0.1442* 7)*4)
 
print(np.round(P7R2,4).real)
print(np.round(P7R27,4).real)
print(np.round(P7R3,4).real)
print(np.round(P7R37,4).real)
print(np.round(P7R4,4).real)

print(np.round((P7R2-P6R27)/P7R2*100,4).real)
print(np.round((P7R27-P6R3)/P7R27*100,4).real)
print(np.round((P7R3-P6R37)/P7R3*100,4).real)
print(np.round((P7R37-P6R4)/P7R37*100,4).real)