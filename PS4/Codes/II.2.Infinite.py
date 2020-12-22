# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 00:24:49 2020

@author: mszta
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy.stats import norm
import time

# Declare the parameters

# Index for utility function
u = 1
sigma = 2       # inverse of the intertemporal elasticity of subsitution
c_bar = 100     # Satiation point for quadratic utility
    
rho = .06
beta = 1/(1+rho)      # discount factor
gamma = 0      # persistence of the process
sigma_y = 0.1   # The standard deviation of the Markov process
N = 2           # The number of income states

# Define the utility function
def U(x):
    if u == 1:
        U = x**(1-sigma)/(1-sigma)
    elif u == 0:
        U = -1/2*(x-c_bar)**2
    return 

m = 1       # mean of the Markov process
# Discretize the Markov chain using the Tauchen algorithm
def tauchen(gamma,sigma_y,N,m):
    Z = np.zeros(N)
    Z_prob = np.zeros((N, N))
    Z[N-1] = (sigma_y**2/(1-gamma**2))**0.5
    Z[0] = -(sigma_y**2/(1-gamma**2))**0.5
    d = (Z[N-1]-Z[0])/(N-1)
    
    ln = np.arange(0,N,1).tolist()
    
    if N==2:
        Z_prob[0][0] = norm.cdf((Z[0] - gamma*Z[0] + d/2)/sigma_y)
        Z_prob[1][0] = norm.cdf((Z[0] - gamma*Z[1] + d/2)/sigma_y)
        Z_prob[0][1] = 1 - norm.cdf((Z[1] - gamma*Z[0] - d/2)/sigma_y)
        Z_prob[1][1] = 1 - norm.cdf((Z[1] - gamma*Z[1] - d/2)/sigma_y)
        
    if N>2:
        for i in ln:
            if i<N-1:
                Z[i+1] = Z[i] + d
            
        for j in ln:
            for k in ln:
                if k == 0:
                    Z_prob[j,k] = norm.cdf((Z[0] - gamma*Z[j] + d/2)/sigma_y)
                elif k == N-1:
                    Z_prob[j,k] = 1 - norm.cdf((Z[N-1] - gamma*Z[j] - d/2)/sigma_y)
                else:
                    Z_prob[j,k] = norm.cdf((Z[k] - gamma*Z[j] + d/2)/sigma_y) - norm.cdf((Z[k] - gamma*Z[j] - d/2)/sigma_y)
        
    return [Z, Z_prob, ln]

if N==2:
    Z = [1-sigma_y, 1+sigma_y]
    Z_prob = [[(1+gamma)/2, (1-gamma)/2], [(1-gamma)/2, (1+gamma)/2]]
    ln = np.arange(0,N,1).tolist()
else:
    [Z, Z_prob, ln] = tauchen(gamma,sigma_y,N)

delta = 0       # the depreciation rate
A = 1       # the production technology
theta = .33     # the capital share

# The initial guess of an interest rate
ret = .04      # the interest rate
r = ret - delta

# Use the first order conditions of the firm to recover K and w
mpk = ret       # define the marginal product of capital         
k = (mpk/theta)**(1/(theta-1))      # recover capital using the FOC of the firm problem
#wage = (1-theta)*k**theta            # recover the wage using the Euler theorem
wage = 1        # wage normalized to 1

# Variable for natural vs no borrowing
borr = 1

# The borrowing constraint
if borr == 1:
    A_low = -Z[0]*1/r     # the natural borrowing constraint
elif borr == 0:
    A_low = 0                   # no borrowing allowed
A_up = 30       # the upper limit on assets

# Set up the asset grid
S = 200          # the size of the asset grid
gs = np.arange(0,S,1).tolist()
grid_ass = np.linspace(A_low,A_up,num = S)      # discretize the asset space


# Preallocate vectors
cfun = np.zeros((S,N))
vfun = np.zeros((S,N))
a_policy = np.zeros((S,N))

min_conv = 10e-3
dev = 1

t = time.time()

# The reward matrix 
if u==1:
    reward = -float('inf')*np.ones((S,S,N))
elif u==0:
    reward = np.zeros((S,S,N))

# Fill the reward matrix and the probability matrix
for z in ln:
    for j in gs:
        for i in gs:
            c = wage*Z[z] + (1+r)*grid_ass[j] - grid_ass[i]
            if c>0 or u==0:
                reward[i,j,z] = U(c)

while dev > 10e-6:
        valueold = vfun
        v = np.zeros((S,S,N))
        
        for j in gs:
            for z in ln:    
                v[:,j,z] = np.matmul(valueold,Z_prob[z][:])
            
        optimand = reward + beta*v
        vfun = np.max(optimand,axis=0)
        a_policy = np.argmax(optimand,axis=0)
        a_policy = a_policy.astype(int)
        for z in ln:
            cfun[:,z] = wage*Z[z] + (1+r)*grid_ass[:] - grid_ass[a_policy[:,z]]
                
        dev = np.max(np.abs(vfun-valueold))
    
elapsed = time.time() - t
print("Ex2e runtime:", elapsed)

# Include in your program a subroutine that simulates paths of consumption and asset holdings
# for the first 45 periods of an agent's life, starting from arbitrary asset position a0 on the grid of assets
# and arbitrary idiosyncratic shock

# Choose arbitrary capital position and shock
a0 = np.int(np.round(S/2))
z0 = np.int(np.round(N/2))

# Initialize the simulation
T = 45      # the simulation horizon
tau = range(1,T)

# Preallocate vectors of consumption and assets
cons_T = np.zeros(T)
ass_T = np.zeros(T+1)
assets_T = np.zeros(T+1)

# Fill the initial values
ass_T[0] = a0
assets_T[0] = grid_ass[np.int(ass_T[0])]
ass_T[1] = a_policy[np.int(a0)][z0]
assets_T[1] = grid_ass[np.int(ass_T[1])]
cons_T[0] = wage*Z[z0] + (1+r)*grid_ass[a0] - assets_T[1]

# Draw random shocks
rng = np.random.default_rng()
Z_t = rng.integers(N, size=T)

for t in tau:
    a = a_policy[np.int(ass_T[t])][Z_t[t]]
    ass_T[t+1] = np.int(a)
    assets_T[t+1] = grid_ass[np.int(a)]
    cons_T[t] = wage*Z[np.int(Z_t[t-1])] + (1+r)*assets_T[t] - assets_T[t+1]
    
# Plots

if u==1:
    # Plot the consumption policy function on the grid of assets
    plt.plot(grid_ass,cfun[:,0],label="Consumption policy for the low aggregate state")
    plt.plot(grid_ass,cfun[:,1],label="Consumption policy for the high aggregate state")  
    plt.suptitle('CRRA Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the T=$\infty$ economy')
    # Place a legend to the right of this smaller subplot.
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.ylabel('Consumption policy')
    plt.xlabel('Assets')
    plt.show()
    
    # Plot the time profile of consumption
    plt.plot(np.linspace(0,T-1,T),cons_T,label="Simulated time profile of consumption in T=$\inf$ economy")
    plt.suptitle('CRRA Consumption simulated time profile for $\sigma_{y}$ = 0.1, $\gamma=0$. in the T=$\infty$ economy')
    plt.ylabel('Consumption')
    plt.xlabel('Time')
    
if u==0:
    # Plot the consumption policy function on the grid of assets
    plt.plot(grid_ass,cfun[:,0],label="Consumption policy for the low aggregate state")
    plt.plot(grid_ass,cfun[:,1],label="Consumption policy for the high aggregate state")  
    plt.suptitle('Quadratic utility Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the T=$\infty$ economy')
    # Place a legend to the right of this smaller subplot.
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.ylabel('Consumption policy')
    plt.xlabel('Assets')
    plt.show()
    
    # Plot the time profile of consumption
    plt.plot(np.linspace(0,T-1,T),cons_T,label="Simulated time profile of consumption in T=$\inf$ economy")
    plt.suptitle('Quadratic utility Consumption simulated time profile for $\sigma_{y}$ = 0.1, $\gamma=0$. in the T=$\infty$ economy')
    plt.ylabel('Consumption')
    plt.xlabel('Time')
    