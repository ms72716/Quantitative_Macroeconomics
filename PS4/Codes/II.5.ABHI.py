# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 00:24:49 2020

@author: mszta
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy.stats import norm  
from scipy import optimize

# Declare the parameters

# Calibration of the model in line with the Handbook of Macroeconomics 
u = 1
sigma = 20       # inverse of the intertemporal elasticity of subsitution
c_bar = 100     # Satiation point for quadratic utility
beta = .9      # discount factor
gamma = 0.4      # persistence of the process
sigma_y = 0.6   # The standard deviation of the Markov process
delta = 0.08       # the depreciation rate
A = 1       # the production technology
theta = .36     # the capital share
N = 20           # The number of income states

# Define the utility function
def U(x):
    if u == 1:
        if sigma == 1:
            U = np.log(x)    
        else:
            U = x**(1-sigma)/(1-sigma)
    elif u == 0:
        U = -1/2*(x-c_bar)**2
    return U


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
    Z1 = Z+1
    return [Z1, Z_prob, ln]

if N==2:
    Z = [1-sigma_y, 1+sigma_y]
    Z_prob = [[(1+gamma)/2, (1-gamma)/2], [(1-gamma)/2, (1+gamma)/2]]
    ln = np.arange(0,N,1).tolist()
else:
    [Z, Z_prob, ln] = tauchen(gamma,sigma_y,N,m)


# Variable for natural vs no borrowing
borr = 0
S = 200          # the size of the asset grid

def Phi(r,opt):
    # Use the first order conditions of the firm to recover K and w
    mpk = r + delta       # define the marginal product of capital         
    k = (mpk/theta)**(1/(theta-1))      # recover capital using the FOC of the firm problem
    wage = (1-theta)*k**theta            # recover the wage using the Euler theorem
    
    # The borrowing constraint
    if borr == 1:
        A_low = -Z[0]*wage/r+0.00001     # the natural borrowing constraint
    elif borr == 0:
        A_low = 0                   # no borrowing allowed
    A_up = 100       # the upper limit on assets
    
    # Set up the asset grid
    gs = np.arange(0,S,1).tolist()
    #grid_ass = numpy.concatenate([np.linspace(A_low,.1*A_up,round(.45*S)),np.linspace(.1*A_up+1/S,.9*A_up,round(.15*S)),np.linspace(.9*A_up+1/S,A_up,round(.4*S))])      # discretize the asset space
    grid_ass = np.linspace(A_low,A_up,S)
    # Preallocate vectors
    cfun = np.zeros((S,N))
    vfun = np.zeros((S,N))
    a_policy = np.zeros((S,N))
    optimand = np.zeros((S,N))
    
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
    
    
    # HOWARD 
    rewardH = np.zeros((S,N))
    H_S = 6        # Specify the iteration when Howard improvements starts
    it = 1
    H = 35        # the number of Howard iterations
    dev = 1
    while dev > 10e-10:
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
            rewardH[:,z] = U(cfun[:,z])

        if it >= H_S:
            for de in np.linspace(0,H,1):
                for y in gs:
                    for z in ln:
                       vfun[y,z] = rewardH[y,z]+beta*np.sum(Z_prob[z][:]*vfun[np.int(a_policy[y,z]),:])
                   
        dev = np.max(np.abs(vfun-valueold))
        it = it+1
        
    trans = np.zeros((N*S,N*S))
    
    for z0 in ln:
        for z1 in ln:
            for i in gs:
                trans[z0*S+i][z1*S+np.int(a_policy[i][z0])] = Z_prob[z0][z1]
    
    # Assume that agents are ex ante homogenous to initialize the transition
    Z_prob_inv = np.ones(S*N)/(S*N)
    
    dv = 1
    
    while dv>10e-8:
        Z_prob_inv_new = np.matmul(trans.transpose(),Z_prob_inv)
        dv = np.max(abs(Z_prob_inv_new-Z_prob_inv))
        Z_prob_inv = Z_prob_inv_new
    
    # Calculate the expected level of assets using the invariant distribution
    A = np.zeros(S*N)
    for s in ln:
        for i in gs:
            A[s*S+i] = Z_prob_inv[s*S+i]*grid_ass[a_policy[i,s]]
    
    EAr = np.sum(A)

    excess_demand = k-EAr

    if opt==1:
        return excess_demand
    elif opt==0:
        afun = grid_ass[a_policy]

        idx = np.argsort(np.ndarray.flatten(afun))
        adist = np.block([ [ Z_prob_inv[idx] ], [ np.sort(np.ndarray.flatten(afun)) ] ])  

        idx = np.argsort(np.ndarray.flatten(cfun))
        cdist = np.block([ [ Z_prob_inv[idx] ], [ np.sort(np.ndarray.flatten(cfun)) ] ])
        
        Z2 = Z_prob
        d=1
        while d>1e-15:
            Z_old=Z2
            Z2 = np.matmul(Z2,Z_prob)
            d = np.max(abs(Z2-Z_old))
            
        Z_erg = Z2[:,1]
        
        return cdist, adist, Z_erg, Z

req = optimize.root_scalar(Phi,args=(1),bracket=[0.0000000001-delta,1/beta-1.00000000001],method='bisect')
[cdist, adist, Z_erg, Z] = Phi(req.root,0)

plt.plot(adist[1,:], adist[0,:],label="asset distribution")
plt.suptitle('Asset distribution for the $\sigma=5$ $\gamma=.6$ $\sigma_{y}=0.4$ parametrization')
# Place a legend to the right of this smaller subplot.
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel('Percent of agents in the group')
plt.xlabel('Asset size group')
plt.show()
    
plt.plot(Z,Z_erg,label="income distribution")
plt.suptitle('Normalized income distribution for the $\sigma=5$ $\gamma=.6$ $\sigma_{y}=0.4$ parametrization')
# Place a legend to the right of this smaller subplot.
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel('Percent of agents in the group')
plt.xlabel('Earnings group')
plt.show()

plt.plot(cdist[1,:], cdist[0,:],label="consumption distribution")
plt.suptitle('The consumption distribution for $\sigma=5$ $\gamma=.6$ $\sigma_{y}=0.4$ parametrization')
# Place a legend to the right of this smaller subplot.
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel('Percent of agents in the group')
plt.xlabel('Expenditure group')
plt.show()

# Calculate asset shares
adist2 = np.zeros((N,N*S))
adist2[0,:] = (adist[0,:]*adist[1,:])/sum(adist[0,:]*adist[1,:])
adist2[1,:] = adist[1,:]

plt.plot(adist2[1,:], adist2[0,:],label="asset distribution")
plt.suptitle('Share of assets owned for the $\sigma=5$ $\gamma=.6$ $\sigma_{y}=0.4$ parametrization')
# Place a legend to the right of this smaller subplot.
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel('Percent of assets owned by the group')
plt.xlabel('Asset size group')
plt.show()

# Calculate consumption shares
cdist2 = np.zeros((N,N*S))
cdist2[0,:] = (cdist[0,:]*cdist[1,:])/(sum(cdist[0,:]*cdist[1,:]))
cdist2[1,:] = cdist[1,:]

plt.plot(cdist2[1,:], cdist2[0,:],label="consumption distribution")
plt.suptitle('Share of total expenditure for the $\sigma=5$ $\gamma=.6$ $\sigma_{y}=0.4$ parametrization')
# Place a legend to the right of this smaller subplot.
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel('Share of consumption by group')
plt.xlabel('Expenditure group')
plt.show()

# Reproduce the table from the Handbook

i = np.int(N*S/5)
A = np.zeros((5,2))

for j in range(0,5):
    A[j,0] = sum(adist2[0,j*i:(j+1)*i-1])
    A[j,1] = sum(cdist2[0,j*i:(j+1)*i-1])