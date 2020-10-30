# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 12:37:18 2020

@author: mszta
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import math
import time

t = time.time()

theta = .679
beta = .988
delta = .013
kappa = 5.24
nu = 2.0

k_lo = 0.01 #lower bound for capital
k_up = 20 #upper bound for capital
S = 200 # number or discrete states between (and including) k_lo and k_up
conv = 1e-6 # convergence criterion %sqrt(eps)

# Steady state
h_ss = (kappa/theta - delta*kappa*(1-theta)/(theta*(1/beta-1+delta)))**(-1/(1/nu+1))
k_ss = h_ss*((1/beta-1+delta)/(1-theta))**(-1/theta)
c_ss = k_ss**(1-theta)*h_ss**theta-delta*k_ss

# Grid for states (capital)
ks = np.linspace(k_lo, k_up, num = S)
gs = np.arange(0,S,1).tolist()

# Period utility
reward = np.matlib.repmat(-float(10**100),S,S)
labour = np.zeros((S,S))
consumption = np.zeros((S,S))

for j in gs:
  for i in gs:
    def f(h):
      return ks[j]**(1-theta)*h**theta+(1-delta)*ks[j]-ks[i]-ks[j]**(1-theta)*h**(theta-1-1/nu)*theta/kappa
    hij = fsolve(f,.1)
    labour[j][i] = hij
    cij = (1-delta)*ks[j]+ks[j]**(1-theta)*hij**theta-ks[i]
    consumption[j][i] = cij
    if cij >= 0: #consumption must be non-negative
      reward[i,j] = math.log(cij)-kappa*((hij)**(1+1/nu))/(1+1/nu)
      
value = np.zeros(S)
cont = np.zeros(S)
kp = np.zeros(S)
cons = np.zeros(S)
l = np.zeros(S)
progress = 1  
it = 1

while progress > conv: #until value function sufficiently changes
    valueold = value
    vold = np.transpose(np.matlib.repmat(valueold, S, 1))
    m = reward+beta*vold
    value = list(np.max(np.array(m), axis=0))
    
    for k in gs:
        cont[k] = np.argmax(m[:,k])
        
    progress = max(abs(np.subtract(value,valueold))) 
    it = it + 1
    
for n in gs:
    idx = np.int(cont[n])    
    kp[n] = ks[idx]
    l[n] = labour[np.int(cont[n])][n]
    cons[n] = consumption[np.int(cont[n])][n]
    
elapsed = time.time() - t
print("Ex2a runtime:", elapsed)
print("Ex2a no. iterations:", it)

plt.plot(ks,value)
plt.xlabel('Capital')
plt.ylabel('Value function')
plt.title('Value function plot 2a_INTRA')
plt.savefig('Value function plot 2a_INTRA.png')
plt.show()    

plt.plot(ks,l)
plt.xlabel('Capital')
plt.ylabel('Labour')
plt.title('Labour policy function plot 2a_INTRA')
plt.savefig('Labour policy function plot 2a_INTRA.png')
plt.show()

plt.plot(ks,cons)
plt.xlabel('Capital')
plt.ylabel('Consumption')
plt.title('Consumption policy function plot 2a_INTRA')
plt.savefig('Consumption policy function plot 2a_INTRA.png')
plt.show()

plt.plot(ks,kp)
plt.xlabel('Capital')
plt.ylabel('Capital policy function')
plt.title('Capital policy function plot 2a_INTRA')
plt.savefig('Capital policy function plot 2a_INTRA.png')
plt.show()
