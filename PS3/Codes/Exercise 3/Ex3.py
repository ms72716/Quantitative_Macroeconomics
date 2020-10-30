# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:40:05 2020

@author: mszta
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import time
import math

t = time.time()

beta = 0.988
delta = 0.013 
theta = 0.679 
nu = 2 
kappa = 5.24
h = 1 
conv = 1e-6 

n = 50 # number of Chebyshev nodes
m = 2 # order of the Chebyshev basis

# Steady state
k_ss = ((1/beta-1+delta)/(1-theta))**(-1/theta)
c_ss = k_ss**(1-theta)-delta*k_ss
# Set upperbound and lowerbound of the state space

k_lo = 5
k_up = k_ss+5

# Compute the collocation points

ks = np.zeros((n,1))
z = np.zeros((n,1))
for j in range(0,n):
    z[j] = -np.cos(np.pi*(2*j-1)/(2*n)) #from interval -1-1
    ks[j] = (z[j]+1)*((k_up-k_lo)/2)+k_lo #adjusted to k_lo and k_up
  
# Basis functions

def basefun(x):
    psi = np.zeros((n,m+1))
    psi[:,0] = 1
    psi[:,1] = x[:,0]
    for i in range(1,m):
        psi[:,i+1] = 2*x[:,0]*psi[:,i]-psi[:,i-1]
    return psi

psi = basefun(ks)
psiZ = basefun(z)

# Initial guess of the coefficients

coef = np.zeros(m+1)
    
# First choose a guess for the level of the value function at collocation points:
    
value = np.matmul(psi,coef)

# Chebyshev regression:
    
for k in range(0,m+1):
    coef[k] = (np.matmul(value,psiZ[:,k]))/(np.matmul(psiZ[:,k],psiZ[:,k]))
    
g = np.zeros(n)
progress = 1    
it = 1
    
while progress > conv:
    coef_old = coef
        
    # Find optimal next period capital from the FOC
    for j in range(0,n):
            def f(kp):
                return ks[j]**(1-theta)*h**theta+(1-delta)*ks[j]-kp-ks[j]**(1-theta)*h**(theta-1-1/nu)*theta/kappa
            g[j] = fsolve(f,0)
        
    ## approximate value:
    value_tylda = np.matmul(psi,coef_old)
        
    for j in range(0,n):
        value[j] = np.log((ks[j]**(1-theta))*(h**theta)+(1-delta)*ks[j]-g[j])-kappa*(1+(1/nu))*(h**(1+(1/nu)))+beta*value_tylda[j]
    
    for k in range(0,m+1):
        coef[k] = (np.matmul(value[:],psiZ[:,k]))/(np.matmul(psiZ[:,k],psiZ[:,k]))
        
    progress = np.max( abs(coef - coef_old )) 
    it = it + 1
     
cons = np.zeros(n)
    
for i in range(0,n):
    cons[i] = ks[i]**(1-theta)*h**theta-g[i]+(1-delta)*ks[i]

elapsed = time.time() - t
print("Ex3 runtime:", elapsed)
print("Ex3 no. iterations:", it)


plt.plot(ks,value)
plt.xlabel('Capital')
plt.ylabel('Value')
plt.title('Value function plot 3')
plt.savefig('Value function plot 3.png')
plt.show()

plt.plot(ks,np.ones(n))
plt.xlabel('Capital')
plt.ylabel('Labour')
plt.title('Labour policy function plot 3')
plt.savefig('Labour policy function plot 3.png')
plt.show()

plt.plot(ks,cons)
plt.xlabel('Capital')
plt.ylabel('Consumption')
plt.title('Consumption policy function plot 3')
plt.savefig('Consumption policy function plot 3.png')
plt.show()

plt.plot(ks,g)
plt.xlabel('Capital')
plt.ylabel('Capital policy function')
plt.title('Capital policy function plot 3')
plt.savefig('Capital policy function plot 3.png')
plt.show()