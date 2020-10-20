# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:22:43 2020

@author: mszta
"""
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import least_squares
import seaborn as sns;
import matplotlib.pyplot as plt
import pandas as pd

rho = .8
omega = 40
gamma = .9
i_0 = .2
N = 1
A_f = 1
kappa_f = .2
kappa_nf = .2
output = np.zeros((101,101))
welfare = np.zeros((101,101))
infections = np.zeros((101,101))
deaths  = np.zeros((101,101))
solution_H_f = np.zeros((101,101));
solution_H_nf = np.zeros((101,101));
beta = np.arange(0, 1.01, 0.01).tolist()
c_tw = np.arange(0, 1.01, 0.01).tolist()
beta_s = np.arange(0, 101, 1).tolist()
ctw_s = np.arange(0, 101, 1).tolist()
x0 = (.5, .5)

for i in beta_s:
    for j in ctw_s:
        def f(x):
            f1 = A_f*(x[0]/(A_f*(x[0])**((rho-1)/rho)+c_tw[j]*A_f*(x[1])**((rho-1)/rho))**(rho/(rho-1)))**(-1/rho)-kappa_f-omega*(1-gamma)*beta[i]*2*i_0*x[0]/N
            f2 = c_tw[j]*A_f*(x[1]/(A_f*(x[0])**((rho-1)/rho)+c_tw[j]*A_f*(x[1])**((rho-1)/rho))**(rho/(rho-1)))**(-1/rho)-kappa_nf
            f3 = x[1]+x[0]-x[2]
            return [f1,f2,f3]
        bound = ((0, 0, 0), (1, 1, 1))
        x0 = [.5,.5, 1]
        x = least_squares(f, x0, bounds=bound)
        x = x.x
        cond = x[0] + x[1]       
    
        if cond<=1:
            x1=x
        
        def g(x):
            return kappa_f/kappa_nf+((2*omega*(1-gamma)*beta[i]*i_0/N)/kappa_nf)*c_tw[j]-x**(-(1+rho)/rho)*(1-x)**(1/rho)
        x = fsolve(g,.5)
        
        def Y(x):
            return (A_f*(x[0])**((rho-1)/rho)+c_tw[j]*A_f*(x[1])**((rho-1)/rho))**(rho/(rho-1))
        
        def I(x):
            return x[0]**2*beta[i]*i_0/N
        
        def U(y):
            return (A_f*(y[0])**((rho-1)/rho)+c_tw[j]*A_f*(y[1])**((rho-1)/rho))**(rho/(rho-1))-kappa_f*y[0]-kappa_nf*y[1]-omega*(1-gamma)*y[0]**2*beta[i]*i_0/N
            
        if cond<=1 and 'x1' in locals():
            if x1[0]>=0 and x1[1]>=0 and x[0]>=0 and x[0]<=1:
                sH1 = [x1[0],x[0]]
                sH2 = [x1[1],1-x[0]]
                UsH = [U([x1[0],x1[1]]),U([x[0],1-x[0]])]
                argmax = np.argmax(UsH)
                s1 = sH1[argmax]
                s2 = sH2[argmax]
                solution_H_f[i][j] = sH1[argmax]
                solution_H_nf[i][j] = sH2[argmax]
        else:
            if 1>=x[0] and x[0]>=0:
                s1 = x[0]
                s2 = 1-x[0]
                solution_H_f[i][j] = s1
                solution_H_nf[i][j] = s2
            else:
                s1 = 0
                s2 = 0
                solution_H_f[i][j] = s1
                solution_H_nf[i][j] = s2
            
        output[i][j]= Y([s1,s2])
        welfare[i][j]= U([s1,s2])
        infections[i][j]= I([s1,s2])
        deaths[i][j]= (1-gamma)*I([s1,s2])

H = solution_H_f+solution_H_nf
H_f_oH = solution_H_f/H
                
H = solution_H_f+solution_H_nf
        
column_names = ['0.00' , '0.01' , '0.02' , '0.03' , '0.04' , '0.05' , '0.06' , '0.07' , '0.08' , '0.09' , '0.10' , '0.11' , '0.12' , '0.13' , '0.14' , '0.15' , '0.16' , '0.17' , '0.18' , '0.19' , '0.20' , '0.21' , '0.22' , '0.23' , '0.24' , '0.25' , '0.26' , '0.27' , '0.28' , '0.29' , '0.30' , '0.31' , '0.32' , '0.33' , '0.34' , '0.35' , '0.36' , '0.37' , '0.38' , '0.39' , '0.40' , '0.41' , '0.42' , '0.43' , '0.44' , '0.45' , '0.46' , '0.47' , '0.48' , '0.49' , '0.50' , '0.51' , '0.52' , '0.53' , '0.54' , '0.55' , '0.56' , '0.57' , '0.58' , '0.59' , '0.60' , '0.61' , '0.62' , '0.63' , '0.64' , '0.65' , '0.66' , '0.67' , '0.68' , '0.69' , '0.70' , '0.71' , '0.72' , '0.73' , '0.74' , '0.75' , '0.76' , '0.77' , '0.78' , '0.79' , '0.80' , '0.81' , '0.82' , '0.83' , '0.84' , '0.85' , '0.86' , '0.87' , '0.88' , '0.89' , '0.90' , '0.91' , '0.92' , '0.93' , '0.94' , '0.95' , '0.96' , '0.97' , '0.98' , '0.99' , '1.00']
row_names    = ['0.00' , '0.01' , '0.02' , '0.03' , '0.04' , '0.05' , '0.06' , '0.07' , '0.08' , '0.09' , '0.10' , '0.11' , '0.12' , '0.13' , '0.14' , '0.15' , '0.16' , '0.17' , '0.18' , '0.19' , '0.20' , '0.21' , '0.22' , '0.23' , '0.24' , '0.25' , '0.26' , '0.27' , '0.28' , '0.29' , '0.30' , '0.31' , '0.32' , '0.33' , '0.34' , '0.35' , '0.36' , '0.37' , '0.38' , '0.39' , '0.40' , '0.41' , '0.42' , '0.43' , '0.44' , '0.45' , '0.46' , '0.47' , '0.48' , '0.49' , '0.50' , '0.51' , '0.52' , '0.53' , '0.54' , '0.55' , '0.56' , '0.57' , '0.58' , '0.59' , '0.60' , '0.61' , '0.62' , '0.63' , '0.64' , '0.65' , '0.66' , '0.67' , '0.68' , '0.69' , '0.70' , '0.71' , '0.72' , '0.73' , '0.74' , '0.75' , '0.76' , '0.77' , '0.78' , '0.79' , '0.80' , '0.81' , '0.82' , '0.83' , '0.84' , '0.85' , '0.86' , '0.87' , '0.88' , '0.89' , '0.90' , '0.91' , '0.92' , '0.93' , '0.94' , '0.95' , '0.96' , '0.97' , '0.98' , '0.99' , '1.00']

# Define data frames
dfH = pd.DataFrame(H, columns=column_names, index=row_names)
dfH_f_oH = pd.DataFrame(H_f_oH, columns=column_names, index=row_names)
dfsolutionH_nf = pd.DataFrame(solution_H_nf, columns=column_names, index=row_names)
dfsolutionH_f = pd.DataFrame(solution_H_f, columns=column_names, index=row_names)
dfoutput = pd.DataFrame(output, columns=column_names, index=row_names)
dfwelfare = pd.DataFrame(welfare, columns=column_names, index=row_names)
dfinfections = pd.DataFrame(infections, columns=column_names, index=row_names)
dfdeaths = pd.DataFrame(deaths, columns=column_names, index=row_names)

# Plots using data frames   
plt.figure(figsize=(9,6))     
ax1 = sns.heatmap(dfsolutionH_f)
plt.title('Heatmap of labour supply on site rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('H_f_2.png')


plt.show() 

plt.figure(figsize=(9,6))
ax2 = sns.heatmap(dfsolutionH_nf)   
plt.title('Heatmap of labour supply telework rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('H_nf_2.png')

plt.show()

plt.figure(figsize=(9,6))
ax3 = sns.heatmap(dfH)
plt.title('Heatmap of employment rate rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('H_2.png')

plt.show()

plt.figure(figsize=(9,6))
ax4 = sns.heatmap(dfH_f_oH)
plt.title('Heatmap of share of on site workers in the labour force rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('H_f_oH_2.png')

plt.show()

plt.figure(figsize=(9,6))
ax5 = sns.heatmap(dfoutput)
plt.title('Heatmap of output rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('output_2.png')

plt.show()

plt.figure(figsize=(9,6))
ax6 = sns.heatmap(dfwelfare)
plt.title('Heatmap of welfare rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('welfare_2.png')

plt.show()

plt.figure(figsize=(9,6))
ax7 = sns.heatmap(dfinfections)
plt.title('Heatmap of infections rho=.8 omega=40', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('infections_2.png')

plt.show()

plt.figure(figsize=(9,6))
ax8 = sns.heatmap(dfdeaths)
plt.title('Heatmap of deaths', fontsize = 20) # title with fontsize 20
plt.xlabel('c_tw', fontsize = 16) # x-axis label with fontsize 15
plt.ylabel('beta', fontsize = 16) # y-axis label with fontsize 15
plt.savefig('deaths_2.png')

plt.show()