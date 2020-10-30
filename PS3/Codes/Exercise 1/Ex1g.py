# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 02:01:19 2020

@author: mszta
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
import time

t = time.time()

H = 50

theta = .679
beta = .988
delta = .013
kappa = 5.24
nu = 2.0

k_lo = 0.01 #lower bound for capital
k_up = 50 #upper bound for capital
S = 300 # number or discrete states between (and including) k_lo and k_up
conv = 1e-6 # convergence criterion %sqrt(eps)

# Steady state
k_ss = ((1/beta-1+delta)/(1-theta))**(-1/theta)
c_ss = k_ss**(1-theta)-delta*k_ss

# Grid for states (capital)
ks = np.linspace(k_lo, k_up, num = S)
gs = np.arange(0,S,1).tolist()

# Period utility
reward = np.matlib.repmat(-float(10**100),S,S)
rewardH = np.zeros(S)
value = np.zeros(S)
cont = np.zeros(S)
cons = np.zeros(S)
kp = np.zeros(S)
progress = 1  
it = 1

for j in gs:
        for i in gs:
            cij = (1-delta)*ks[j]+ks[j]**(1-theta)-ks[i]
            if cij >= 0: #consumption must be non-negative
                reward[i,j] = math.log(cij)-kappa/(1+1/nu)

while progress > conv: #until value function sufficiently changes
    valueold = value
    vold = np.transpose(np.matlib.repmat(valueold, S, 1))
    m = reward+beta*vold
    value = list(np.max(np.array(m), axis=0))
    
    for k in gs:
        cont[k] = np.argmax(m[:,k])
        rewardH[k] = reward[np.int(cont[k])][k]

        for u in np.linspace(0,H,1):
            for y in gs:
                value[y] = rewardH[y]+beta*value[np.int(cont[y])]
        
    progress = max(abs(np.subtract(value,valueold))) 
    it = it + 1
    
for n in gs:
    idx = np.int(cont[n])    
    kp[n] = ks[idx]
    cons[n] = ks[n]**(1-theta)-kp[n]+(1-delta)*ks[n]

elapsed = time.time() - t
print("Ex1f runtime:", elapsed)
print("Ex1f no. iterations:", it)

plt.plot(ks,value)
plt.xlabel('Capital')
plt.ylabel('Value')
plt.title('Value function plot 1f')
plt.savefig('Value function plot 1f.png')
plt.show()

plt.plot(ks,np.ones(S))
plt.xlabel('Capital')
plt.ylabel('Labour')
plt.title('Labour policy function plot 1f')
plt.savefig('Labour policy function plot 1f.png')
plt.show()

plt.plot(ks,cons)
plt.xlabel('Capital')
plt.ylabel('Consumption')
plt.title('Consumption policy function plot 1f')
plt.savefig('Consumption policy function plot 1f.png')
plt.show()

plt.plot(ks,kp)
plt.xlabel('Capital')
plt.ylabel('Capital policy function')
plt.title('Capital policy function plot 1f')
plt.savefig('Capital policy function plot 1f.png')
plt.show()


