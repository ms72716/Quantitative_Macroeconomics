# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 00:24:49 2020

@author: mszta
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt

from scipy.stats import norm

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
min_conv = 1e-6     # the convergence criterion

# The initial guess of an interest rate
ret = 0.04      # the interest rate
r = ret - delta

# Use the first order conditions of the firm to recover K and w
mpk = ret         # define the marginal product of capital         
k = (mpk/theta)**(1/(theta-1))      # recover capital using the FOC of the firm problem
#wage = (1-theta)*k**theta            # recover the wage using the Euler theorem
wage = 1        # wage normalized to 1

T = 45      # duration/number of cohorts
S = 200          # the size of the asset grid
gs = np.arange(0,S,1).tolist()

# Variable for natural vs no borrowing
borr = 1

# The borrowing constraint
A_up = 30       # the upper limit on assets

if borr == 1:
    grid_ass = np.zeros((S,T))
    # In the OLG the natural borrowing limit is cohort-specific
    for c in range(0,T):
        A_low = -Z[0]*(1/r)*(1-(1+r)**(c-T))
        # Set up the asset grid
        grid_ass[:,c] = np.linspace(A_low,A_up,num = S)      # discretize the asset space
elif borr == 0:
    A_low = 0                   # no borrowing allowed
    # Set up the asset grid
    grid_ass = np.linspace(A_low,A_up,num = S)      # discretize the asset space


# Preallocate vectors
cfun = np.zeros((T,N,S))
vfun = np.zeros((T,N,S))
vpfun = np.zeros(S)
vptrans = np.zeros((T,N,S))
a_policy = np.zeros((T,N,S))
optimand = np.zeros((S,S))

if borr == 0:

    for t in np.arange(T-1, 0, -1):
         # If we are in the last period
         if t==T-1:   
             for z in ln:
                # Final period Consumption function, asset holdings, value function, including derivative
                cfun[t,z,:] = grid_ass[:] + wage*Z[z]
                a_policy[t,z,:] = 0
                for i in gs:
                    if cfun[t,z,i]>0 or u==0:
                        vfun[t,z,:] = U(cfun[t,z,:])
                    else:
                        vfun[t,z,i] = -float('inf')
         else:
             for z in ln:
                 for i in gs:
                     for j in gs:
                         c = wage*Z[z] + (1+r)*grid_ass[i] - grid_ass[j]
                         if c>0 or u==0:
                             optimand[j,i] = U(c)+beta*np.sum(Z_prob[z][:]*vfun[t+1,:,j])
                         else:
                             optimand[j,i] = -float('inf')
                 vfun[t,z,:] = np.max(optimand,axis=0)
                 for i in gs:
                     a_policy[t,z,i] = np.argmax(optimand[:,i])
                     cfun[t,z,i] = wage*Z[z] + (1+r)*grid_ass[i] - grid_ass[np.int(a_policy[t,z,i])]
                     
    # Plot the consumption function for T=5 and T=40
    plt.plot(grid_ass,cfun[5,1,:],label="Consumption policy for cohort 5")
    plt.plot(grid_ass,cfun[40,1,:],label="Consumption policy for cohort 40")        
    plt.suptitle('Consumption policy function on the grid of assets for $\sigma_{y}$ = 0. in the 45 period OLG')
    # Place a legend to the right of this smaller subplot.
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
elif borr == 1:
        
    for t in np.arange(T-1, -1, -1):
         # If we are in the last period
         if t==T-1:   
             for z in ln:
                # Final period Consumption function, asset holdings, value function, including derivative
                cfun[t,z,:] = (1+r)*grid_ass[:,t] + wage*Z[z]
                a_policy[t,z,:] = 0
                for i in gs:
                    if cfun[t,z,i]>0 or u==0:
                        vfun[t,z,i] = U(cfun[t,z,i])
                    else:
                        vfun[t,z,i] = -float('inf')
         else:
             for z in ln:
                 for i in gs:
                     for j in gs:
                         c = wage*Z[z] + (1+r)*grid_ass[i,t] - grid_ass[j,t+1]
                         if c>0 or u==0:
                             optimand[j,i] = U(c)+beta*np.sum(Z_prob[z][:]*vfun[t+1,:,j])
                         else:
                             optimand[j,i] = -float('inf')
                 vfun[t,z,:] = np.max(optimand,axis=0)
                 for i in gs:
                     a_policy[t,z,i] = np.argmax(optimand[:,i])
                     cfun[t,z,i] = wage*Z[z] + (1+r)*grid_ass[i,t] - grid_ass[np.int(a_policy[t,z,i]),t+1]
                     
    # Run a 45 period simulation
    
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
    assets_T[0] = grid_ass[np.int(ass_T[0]),0]
    ass_T[1] = a_policy[0,z0,np.int(a0)]
    assets_T[1] = grid_ass[np.int(ass_T[1]),1]
    cons_T[0] = wage*Z[z0] + (1+r)*assets_T[0] - assets_T[1]
    
    # Draw random shocks
    rng = np.random.default_rng()
    Z_t = rng.integers(N, size=T)
    
    for t in tau:
        a = a_policy[t][Z_t[t]][np.int(ass_T[t])]
        ass_T[t+1] = np.int(a)
        assets_T[t+1] = grid_ass[np.int(a),t]
        cons_T[t] = wage*Z[np.int(Z_t[t-1])] + (1+r)*assets_T[t] - assets_T[t+1]
        
    if u == 1:
        # Plot the consumption function for T=5 and T=40
        plt.plot(grid_ass[:,5],cfun[5,1,:],label="Consumption policy for cohort 5")
        plt.suptitle('CRRA Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        # Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption policy')
        plt.xlabel('Assets')
        plt.show()
        
        plt.plot(grid_ass[:,40],cfun[40,1,:],label="Consumption policy for cohort 40")        
        plt.suptitle('CRRA Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        # Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption policy')
        plt.xlabel('Assets')
        plt.show()
        
        plt.plot(grid_ass[:,5],cfun[5,1,:],label="Consumption policy for cohort 5")
        plt.plot(grid_ass[:,40],cfun[40,1,:],label="Consumption policy for cohort 40")  
        plt.suptitle('CRRA Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        # Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption policy')
        plt.xlabel('Assets')
        plt.show()
        
        # Plot the time profile of consumption
        plt.plot(np.linspace(0,T-1,T),cons_T,label="simulated consumption over time")
        plt.suptitle('CRRA Consumption simulated time profile for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption')
        plt.xlabel('Time')
    elif u == 0:
        # Plot the consumption function for T=5 and T=40
        plt.plot(grid_ass[:,5],cfun[5,1,:],label="Consumption policy for cohort 5 and the high state")
        plt.plot(grid_ass[:,5],cfun[5,0,:],label="Consumption policy for cohort 5 and the low state")
        plt.suptitle('Cohort 5 Quadratic utility Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        # Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption policy')
        plt.xlabel('Assets')
        plt.show()
        
        plt.plot(grid_ass[:,40],cfun[40,1,:],label="Consumption policy for cohort 40 and the high state") 
        plt.plot(grid_ass[:,40],cfun[40,0,:],label="Consumption policy for cohort 40 and the low state") 
        plt.suptitle('Cohort 40 Quadratic utility Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        # Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption policy')
        plt.xlabel('Assets')
        plt.show()
        
        plt.plot(grid_ass[:,5],cfun[5,1,:],label="Consumption policy for cohort 5 and the high state")
        plt.plot(grid_ass[:,5],cfun[5,0,:],label="Consumption policy for cohort 5 and the low state")
        plt.plot(grid_ass[:,40],cfun[40,1,:],label="Consumption policy for cohort 40 and the high state") 
        plt.plot(grid_ass[:,40],cfun[40,0,:],label="Consumption policy for cohort 40 and the low state") 
        plt.suptitle('Cohort 5 and 40 Quadratic utility Consumption policy function on the grid of assets for $\sigma_{y}$ = 0.1, $\gamma=0$. in the 45 period OLG')
        # Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption policy')
        plt.xlabel('Assets')
        plt.show()
        
         # Plot the time profile of consumption
        plt.plot(np.linspace(0,T-1,T),cons_T,label="simulated consumption over time")
        plt.suptitle('Quadratic utility Consumption simulated time profile for $\sigma_{y}$ = 0.1, $\gamma=0$.  in the 45 period OLG')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.ylabel('Consumption')
        plt.xlabel('Time')
             
                 