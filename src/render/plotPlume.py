#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:50:44 2022

@author: ggronchi
"""
import numpy as np
import matplotlib.pyplot as plt
import os

def plot(exp_dir, render_namelist, ambient_namelist):

    # Default plots :
        #   trajectory and envelope in z-x, z-y planes
        #   dynamics z-t
        #   radius 
        #   oil concetration
    
    # Custom plots :
        # Cylinder properties:      mass
        #                           orientation
        #                           vertical velocity
        # Entrainment properties:   entraining volume fluxes,
        #                           shear entrainment coeff alpha
        # Buoyancy properties:      plume and ambient density difference     

    ns_flag=False
    
    if ambient_namelist['SEA_AREA']=='NORTHSEA':
        ns_flag = True

    modelf = np.loadtxt(rf'{exp_dir}/plumeState.csv', comments='#', delimiter='\t',skiprows=1)
    paramf = np.loadtxt(rf'{exp_dir}/parameters.csv', comments='#', delimiter='\t',skiprows=1)

    if ns_flag == True:
        dataf = np.loadtxt('./examples/NORTHSEA/envFields/northsea_obs.txt', comments='#')
        time_data = dataf[:,0]
        depth_data = dataf[:,1]
        sx_sim = dataf[:,2]
        dx_sim = dataf[:,3]
        sx_data = dataf[:,4]
        dx_data = dataf[:,5]

    time = modelf[:,0]   
    mass = modelf[:,1]   
    u = modelf[:,2]
    w = modelf[:,3]  
    c = modelf[:,4]              
    x = modelf[:,9]
    y = modelf[:,10]
    z = modelf[:,11]
    r = modelf[:,8]
    h = modelf[:,7]
    rho = modelf[:,5]
    rhoa = modelf[:,6]
    
    alpha=paramf[:,1]
    vaproj=paramf[:,2]
    V0=paramf[:,3]
    rhoa1 = paramf[:,4]
    Qs=paramf[:,5]
    Qf=paramf[:,6]
    Qe = paramf[:,7]
    phi = paramf[:,8]
    g1 = paramf[:,9]
    Fd2 = paramf[:,10]

    plt.clf() #avoid overplot


    # Default plots:

    # Plume trajectory and envelope 

    fig,ax = plt.subplots()

    plt.plot(x,z, color='k', linestyle='dashed')
    plt.plot(x+r, z, color='k')
    plt.plot(x-r, z, color='k', label='UWORM-1 model')
   

    if ns_flag == True: # add observations plot for the North Sea exp
        plt.hlines(-55,-10.,50., colors='grey', linewidth=40, alpha=0.2)
        plt.plot(sx_data, depth_data , 'g', label='NOFO data', alpha=0.5 )
        plt.plot(dx_data, depth_data, 'g', alpha=0.5)
        plt.plot(sx_sim, depth_data, 'red', label='Yapa model (1999)', alpha=0.5)
        plt.plot(dx_sim, depth_data, 'red', alpha=0.5)
        plt.xlabel('South-East displacement (m)')
        plt.xlim(-10,45)


    plt.grid(visible=None, which='major', axis='both', alpha=0.4)
    plt.ylabel('Depth [m]',fontsize=12)
    plt.xlabel('Zonal axis [m]',fontsize=12)
    plt.ylim(z[0],0)

    plt.legend(loc='lower right')
    plt.savefig('{}traj_env_xz.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
    


    fig,ax = plt.subplots()

    plt.plot(y,z, color='k', linestyle='dashed')
    plt.plot(y+r, z, color='k')
    plt.plot(y-r, z, color='k')
   
    plt.grid(visible=None, which='major', axis='both', alpha=0.4)
    plt.ylabel('Depth [m]',fontsize=12)
    plt.xlabel('Meridional axis [m]', fontsize=12)
    plt.ylim(z[0],0)
    plt.legend(loc='lower right')
    plt.savefig('{}traj_env_yz_.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
    


    # Plume dynamics 

    fig = plt.figure()
    plt.grid(visible=None, which='major', axis='both', alpha=0.4)

    plt.plot(time, z, 'k')
    if ns_flag == True:
        plt.scatter(time_data, depth_data, label ='NOFO data', marker='.', s=70, color='g')
        plt.hlines(-55,-2.,10., colors='grey', linewidth=40, alpha=0.2)
        plt.legend(loc='lower right')

    plt.xlabel('Time [min]', fontsize='12')
    plt.ylabel('Depth [m]',fontsize='12')
    plt.ylim([z[0],0])
    plt.savefig('{}dyn.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
    


    # Plume radius

    fig = plt.figure()
    plt.grid(visible=None, which='major', axis='both', alpha=0.4)
    plt.plot(r, z, 'k')
    plt.xlabel('Plume radius [m]',fontsize='12')
    plt.ylabel('Depth [m]',fontsize='12')
    plt.savefig('{}radius.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
    


    # Plume position and oil concentration 

    fig,ax = plt.subplots(figsize=(9, 6))
    lns1 = ax.plot(time, c, 'r', label = 'c')

    ax2 = ax.twinx()
    lns2 = ax2.plot(time, w, 'k', label = 'w')

    ax.set_yscale("log")
    #ax.set_xscale("log")
  
    lns = lns1+lns2
    labs =[l.get_label() for l in lns]
    ax.legend(lns, labs, loc='best')

    ax.grid(alpha=0.4)
    ax.set_xlabel("Time [min]",fontsize=14)
    ax2.set_ylabel('Vertical velocity [m/s]',fontsize='14')
    ax2.tick_params(axis='both', which='major', labelsize=13)
    ax.set_ylabel('Oil concentration [adim]',fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=13)
    plt.savefig('{}oilconc_vel.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
 




    # # Custom plots: cylinder

    custom_cylinder = render_namelist.custom_cylinder
    if (custom_cylinder == True):


        # Cylinder mass
        fig = plt.figure()
        plt.grid(visible=None, which='major', axis='both', alpha=0.4)
        plt.plot(time, mass, 'k')
        plt.ylabel(' Mass [kg]',fontsize='12')
        plt.xlabel('Time [min]',fontsize='12')
        plt.yscale('symlog')
        plt.savefig('{}mass.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
        


        # Cylinder orientation
        fig = plt.figure()
        plt.grid(visible=None, which='major', axis='both', alpha=0.4)
        plt.plot(time, phi/3.14*180, 'k')
        plt.ylabel('$v_{\phi}$ [$^\circ$]',fontsize='12')
        plt.xlabel('Time [min]',fontsize='12')
        plt.savefig('{}bending.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)


        # Cylinder vertical velocity
        fig = plt.figure()
        plt.grid(visible=None, which='major', axis='both', alpha=0.4)
        plt.plot(time, w, 'k')
        plt.xlabel('Time [min]',fontsize='12')
        plt.ylabel('w [m/s]',fontsize='12')
        plt.savefig('{}vertical_vel.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)

    

    # # Custom plots: entrainment

    custom_entrain = render_namelist.custom_entrain
    if (custom_entrain == True):

        # Entraining fluxes

        fig= plt.figure()
        plt.grid(visible=None, which='major', axis='both',alpha=0.2)
        plt.plot( time, Qf, label='$Q_f$', color='red')
        plt.plot( time, Qs, label='$Q_s$', color='b')
        plt.plot( time, Qe, label='$Q_e$', color='k')
        plt.ylabel('Volume flux $(m^3 s^{-1})$')
        plt.xlabel('Time (min)')
        plt.legend()
        plt.savefig('{}fluxes.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)
     


        # Shear coefficient alpha

        fig = plt.figure()
        plt.grid(visible=None, which='major', axis='both',alpha=0.2)
        plt.plot(1/Fd2, alpha, 'k')
        plt.ylabel('shear entrainment coeff [adim]')
        plt.xlabel('$F_d^{-2}$ [adim]')
        plt.xlim(-1,0.5)
        plt.ylim(-0.5,0.5)
        plt.savefig('{}shear_entrain_coeff.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)



    # Custom plots: buoyancy

    custom_buoyancy = render_namelist.custom_buoyancy
    if (custom_buoyancy == True):

        fig,ax = plt.subplots(figsize=(10,10))
        lns1 = ax.plot(time, g1, 'r', label = 'Reduced Gravity')
        ax.set_ylim(g1.min()-0.0010,-g1.min()+0.0010)
        ax2 = ax.twinx()
        lns2 = ax2.plot(time, w, 'k', label = 'Vertical Velocity')
        ax2.set_ylim(-0.2, 0.2)
        #ax2.set_yscale("log")


        lns = lns1+lns2
        labs =[l.get_label() for l in lns]
        ax.legend(lns, labs, loc=0)
        #ax.set_yscale("log")
        ax.grid(alpha=0.4)
        ax.set_xlabel("Time [min]",fontsize=14)
        ax.set_ylabel(r'$g^{l} \: [m s^{-2}]$',fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax2.set_ylabel(' w $ \: [m s^{-1}]$',fontsize=14)
        ax2.tick_params(axis='both', which='major', labelsize=13)
        
        plt.savefig('{}reduced_gravity.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)


        # Froude number square

        fig = plt.figure()
        plt.grid(visible=None, which='major', axis='both',alpha=0.2)
        plt.plot(time, 1/Fd2, 'k')
        plt.ylabel('$F_d^{-2}$ [adim]')
        plt.xlabel('Time [min]')
        plt.ylim(-1,0.5)
        plt.savefig('{}froude.png'.format(os.path.join(exp_dir, 'PICS' + '/')), dpi=300)






