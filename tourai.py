import math

c=3.0*10**8

#A,Bの距離差(ns)
tab=-0.3

#B,Cの距離差(ns)
tbc=0.5

#最小目盛り(ns)
memori=0.4

x=memori/2

#phiは逆から来てる可能性がある
phi=math.degrees(math.atan(tbc/tab))
theta=math.degrees(math.asin(0.3*math.sqrt(tab**2+tbc**2)))

print(phi)
print(theta)

deltaphi=math.degrees((x)/(math.sqrt(tab**2+tbc**2)))
deltatheta=math.degrees((0.3*x)/(math.sqrt(6.25-0.09*(tab**2+tbc**2))))

print(deltaphi)
print(deltatheta)
