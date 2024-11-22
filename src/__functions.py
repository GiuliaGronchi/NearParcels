#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Jul 22 17:12:41 2021
@author: giulia

'''

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator
import gsw
import os

# # Calculation of reduced gravity
def reduced_g(params):
    ''' 
    The reduced gravity g1 is calculated by rescaling the gravity acceleration g
    to the density difference between plume and ambient water
    '''
    g1 = params['g'] * (params['rhoa'] - params['rho'])/params['rhoa_0']
    return g1

# # Calculation of projected velocity differences
def proj_vel(params):
    '''
    The projection proj_vel of the cylinder velocity v on the ambient ocean velocity v_a is computed
    '''
    ua=params['ua']
    va=params['va']
    u=params['u']
    v=params['v']
    v_0=params['v_0']

    vel = np.array([u,v])
    a_vel = np.array([ua,va])   
    proj_vel=np.dot(vel,a_vel)/v_0

    return proj_vel

def vdif(params):
    '''
    The difference between the plume velocity and the proj_vel will be used in the shear flux computation.
    '''
    vdif=np.abs(params['v_0']  - proj_vel(params))  

    return vdif

# # Computation of the shear flux
def shear_entrain_yapa(params):
    '''
    The shear component Qs of the entrainment flux is proportional to:
    - the cylinder lateral surface
    - the shear with the ambient currents represented by vdif
    - entrainment coefficient alpha
    '''
    b=params['b']   
    h=params['h']  
    alpha=params['alpha'] 

    # shear entrainment following Yapa et al., (1997)                        
    Qs = 2 * np.pi * b * h * alpha * vdif(params)

    return Qs

# # Computation of the entrainment coefficient
def entrain_coeff_yapa(params):
    '''
    The entrainment coefficient alpha used in the shear component is empirically derived.
    It contains the plume orientation v_phi, the densimetric Froude number F1 and the vdif, 
    with empirical coefficients a1,a2,a3.
    '''
    a1 = params['a1']
    a2 = params['a2']
    a3 = params['a3']
    b=params['b']
    v_phi=params['v_phi']  

    invF1_square = reduced_g(params) * b*2 /(vdif(params))**2
    alpha = ( a1 + a2 * np.sin(v_phi) * invF1_square ) / (1 + a3 * proj_vel(params) / vdif(params))
  
    return alpha


# # Computation of the forced flux
def forced_entrain_yapa(params):
    '''
    The forced component Qf of the entrainment flux is the ocean currents transport onto the windward surface of the plume.
    The zonal and meridional components are sources for Qfx, Qfy respectively.
    The calculation considers deformations of the cylinder surface (stretching, bending, and enlargement).
    '''
    ua=params['ua']
    va=params['va']
    b=params['b']    
    v_phi=params['v_phi']  
    v_theta=params['v_theta']   
    bb=params['bb']
    v_phib=params['v_phib']  
    v_thetab=params['v_thetab'] 
    ds=params['ds']
    
    Qfx = np.abs(ua) * ( np.pi * b * (b-bb)* np.absolute(np.cos(v_theta)*np.cos(v_phi)) + \
                2 * b* ds * np.sqrt(1 - np.cos(v_theta)**2 * np.cos(v_phi)**2 ) + \
                np.pi * b**2 /2 * np.absolute(np.cos(v_theta)*np.cos(v_phi)-np.cos(v_thetab)*np.cos(v_phib)) )
    Qfy = np.abs(va) * ( np.pi * b * (b-bb)* np.absolute(np.sin(v_theta)*np.cos(v_phi)) + \
                2 * b* ds * np.sqrt(1 - np.sin(v_theta)**2 * np.cos(v_phi)**2 ) + \
                np.pi * b**2 /2 * np.absolute(np.sin(v_theta)*np.cos(v_phi)-np.sin(v_thetab)*np.cos(v_phib)) )  
    Qf= np.abs(Qfx) + np.abs(Qfy)

    return Qf


# # GOVERNING EQUATIONS
# # Calculation of dx, where plume_state = ( m, um, vm, wm, cm, x, y, z, Tm, Sm ) 
def model(plume_state,params):

    '''The plume state is updated following the governing equations: 
    - mass conservation for m
    - momentum conservation for (um,vm,wm)
    - oil mass conservation for m_oil = cm
    - tracking position x,y,z
    - heat conservation (c_p T m)
    - salt mass conservation Sm
    '''
       
    rhoa=params['rhoa']
    ua=params['ua']
    va=params['va']
    ca=params['ca']
    Ta=params['Ta']
    Sa=params['Sa']
    g1 = params['g1'] 
    
    Qs=shear_entrain_yapa(params)
    Qf=forced_entrain_yapa(params)
    
    if params['total_entrain']==0:
        Qe = max(Qs,Qf)
    elif params['total_entrain']==1:
        Qe = Qs + Qf

    plume_state_timevar=np.array([rhoa * Qe, (rhoa * Qe)*ua,  (rhoa * Qe)*va , plume_state[0] * g1, rhoa * Qe * ca , \
                   plume_state[1]/plume_state[0], plume_state[2]/plume_state[0], plume_state[3]/plume_state[0], rhoa* Qe * Ta, rhoa * Qe * Sa]) 

    return plume_state_timevar


# # RUNGE-KUTTA IV 
def RK4(model,params,plume_state_b,dt):  
      
    k1=dt*model(plume_state_b,params)
    k2=dt*model(plume_state_b + k1/2, params)
    k3=dt*model(plume_state_b + k2/2, params)
    k4=dt*model(plume_state_b + k3, params)
    d_plume_state=1/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    return d_plume_state
