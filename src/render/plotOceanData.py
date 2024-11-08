import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import os




def plot_ocean(exp_dir, ambient_namelist):
    # # # Read ocean horizontally interpolated variables from cmems # # #
    df=pd.read_csv('{}oceanProfilesInput.csv'.format(os.path.join(exp_dir + '/')))
    depth=df['depth']
    thetao=df['thetao']
    so=df['so']
    rhoa=df['rhoa']
    uo=df['uo'] 
    vo=df['vo']

    ns_flag=False
    if ambient_namelist['SEA_AREA']=='NORTHSEA':
        ns_flag = True
    

    if ns_flag == True:
        uo=df['uo']*np.cos(np.pi/2) - df['vo']*np.sin(np.pi/2)
        vo=df['uo']*np.sin(np.pi/2) - df['vo']*np.cos(np.pi/2)

    # Interpolation of temperature, salinity, density in depth
    f_uo = interp1d(depth, uo)
    f_vo = interp1d(depth, vo)
    f_thetao = interp1d(depth, thetao)
    f_so = interp1d(depth, so)
    f_rhoa = interp1d(depth, rhoa)
    

    # density PLOT
  
    plt.grid(visible=None, which='major', axis='both')
    zp = np.linspace(depth.iloc[-1], -2, 100)
    fig = plt.subplots(figsize=(4, 7))
    plt.gcf().subplots_adjust(left=0.15)
    plt.grid(visible=None, which='major', axis='both')
    plt.plot(f_rhoa(zp)-1000,zp, color='black', label='Density')
    plt.ylabel('Depth (m)', fontsize=14)
    plt.xlabel('$\sigma$ $(kg \, m^{-3})$', fontsize=14)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend()
    plt.savefig('{}ambient_density.png'.format(os.path.join(exp_dir + '/')), dpi=300)

    # temperature and salinity PLOT

    fig, ax1 = plt.subplots(figsize=(5, 7))
    #plt.tight_layout()
    plt.gcf().subplots_adjust(left=0.25)
    ax1.grid()
    ax1.plot(f_thetao(zp),zp, color='black', label='Temperature')
    ax1.set_xlabel('T ($^\circ C$)',fontsize=14)
    ax1.set_ylabel('Depth (m)',fontsize=14)
    ax1.legend(loc='lower left')
    ax1.tick_params(axis='both', which='major', labelsize=13)
    ax2 = ax1.twiny()
    ax2.grid(alpha=0.2)
    ax2.plot(f_so(zp),zp, color='blue', label='Salinity')
    ax2.set_xlabel('S (psu)',fontsize=14)
    ax2.legend(loc='lower right')
    ax2.tick_params(axis='both', which='major', labelsize=13)
    fig.savefig('{}ambient_tempsal.png'.format(os.path.join(exp_dir + '/')), dpi=300)
    
    
    # currents PLOT

    fig = plt.subplots(figsize=(4, 7))
    plt.gcf().subplots_adjust(left=0.15)
    plt.grid(visible=None, which='major', axis='both')
    plt.plot(f_uo(zp),zp, color='black', label='u zonal')
    plt.plot(f_vo(zp),zp, color='blue', label='v meridional')
    plt.ylabel('Depth (m)',fontsize=14)
    plt.xlabel('Ocean Velocity $(m \, s^{-1}$)',fontsize=14)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlim(-0.15,0.15)
    plt.legend()
    plt.savefig('{}ambient_currents.png'.format(os.path.join(exp_dir + '/')), dpi=300)