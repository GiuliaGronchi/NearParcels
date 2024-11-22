#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.utils.output_db import compute_and_save_product_summary
from src.utils.utils import print_ntime, tqdm_green

'''
Created on Thu Jul 22 17:12:41 2021
@author: giulia

This code simulates the near-field stage of a subsurface spill.
The plume is simulated as independent cylinders whose mass grows in time according to the \
entrainment of seawater through turbulent votices at the plume edges.

The plume cylinder state (mass, u, v, w, c, x,y,z, T, S)
is updated with the governing equations, solved with a RK4 scheme
Then other variables are disgnostically computed as radius, thickness, density
Ocean input variables are currents, temperature and salinity (from Copernicus Service)

'''

from src.__functions import *


def plume(exp_dir, runId, ambient_namelist, numerical_namelist, release_namelist, constants):

    # # # Read ocean data vertical profiles # # #
    df = pd.read_csv('{}oceanProfilesInput.csv'.format(os.path.join(exp_dir + '/')))
    depth=df['depth']
    thetao=df['thetao']
    so=df['so']
    rhoa=df['rhoa']
    

    if ambient_namelist['SEA_AREA']=='NORTHSEA':
         uo=df['uo']*np.cos(np.pi/2) - df['vo']*np.sin(np.pi/2)
         vo=df['uo']*np.sin(np.pi/2) - df['vo']*np.cos(np.pi/2)
    else:
        uo=df['uo']
        vo=df['vo']
         

    # Interpolation of temperature, salinity, density in depth

    f_uo = interp1d(depth, uo)
    f_vo = interp1d(depth, vo)
    f_thetao = interp1d(depth, thetao)
    f_so = interp1d(depth, so)
    f_rhoa = interp1d(depth, rhoa)

         

    # Natural constants
    
    g=constants.g
    c_T=constants.c_T
    ca=constants.c_a

    p = {'g': g, 'c_T': c_T, 'ca': ca}

    p['total_entrain'] = numerical_namelist['entrain_params']['total_entrain']  # if 0 max(Qs,Qf); if 1 sum(Qs,Qf)
    for a in ['a1', 'a2', 'a3']:
        p[a] = numerical_namelist['entrain_params'][a]

    max_height = None
    neu_buoy = None

    

    # total simulation time (minutes)
    time_max = numerical_namelist.time_max
    # time-step of integration (seconds)
    dt = numerical_namelist.dt  # or dt=10*p['b']/p['V']
    # total number of generated cylinders
    ncyl = numerical_namelist.ncyl

    # SET THE INITIAL CONDITIONS

    # Release parameters initialization :
    # depth, position, oil concentration, temperature, salinity, velocity, radius
    
    z0 = release_namelist.z0
    x0 = release_namelist.x0
    y0 = release_namelist.y0
    c0 = release_namelist.c0
    T0 = release_namelist.T0
    S0 = release_namelist.S0
    u0 = release_namelist.u0
    v0 = release_namelist.v0
    w0 = release_namelist.w0
    b0 = release_namelist.b0

    # Oil density at reference temperature
    # Crude oil Troll API 35.8 = 843 kg/m3 at 15.5 C
    rho_oil_0 = release_namelist.rho_oil_0
    T_oil_0 = release_namelist.T_oil_0



    # A cylinder is generated (just one for instantaneous release)
    for cyl in range (0, ncyl): #range(0,tmax)
        print_ntime(f'Cylinder #{cyl+1}/{ncyl}')
        # total number of time-steps
        tmax = int(time_max*60/dt)

        # Other plume parameters initialization
        p['h'] = w0*dt
        p['u'], p['v'] = u0, v0
        p['b'], p['bb'] =  b0, b0
        p['v_0'], p['v_0b'] = np.sqrt(u0**2 + v0**2 + w0**2), np.sqrt(u0**2 + v0**2 + w0**2)
        p['ds'] = p['v_0'] *dt
        p['v_phi'], p['v_phib'] = np.arcsin(w0/p['v_0']), np.arcsin(w0/p['v_0'])
        p['v_theta'], p['v_thetab'] = np.arctan2(v0,u0), np.arctan2(v0,u0)

        # Ambient parameters initialization : temperature, salinity, density, zonal and meridional currents
        p['Ta'], p['Sa'], p['rhoa'], p['rhoa_0'] = float(f_thetao(z0)), float(f_so(z0)), float(f_rhoa(z0)), float(f_rhoa(z0))
        p['ua'], p['va'] = float(f_uo(z0)), float(f_vo(z0))

        # Oil and plume density, reduced gravity
        p['rho_oil'] = rho_oil_0 * (1 - p['c_T'] * (T0 - T_oil_0 ))
        p['rho_w'] = gsw.density.rho(S0,T0,1)
        p['rho'] = p['rho_oil'] * p['rho_w'] / (p['rho_w'] * c0 + p['rho_oil'] * (1 - c0))
        p['g1'] = reduced_g(p)

        # Entrainment first computation
        p['alpha'] = entrain_coeff_yapa(p)
        Qs = shear_entrain_yapa(p)
        Qf = forced_entrain_yapa(p)
        if p['total_entrain'] == 0:
                    Qe = max(Qs,Qf)
        elif p['total_entrain'] == 1:
                    Qe = Qs + Qf
        
        

        # Cylinder mass initialization
        m0 = p['rho_oil']* np.pi * p['b']**2 * p['h']
        oil_volume0 = m0/p['rho_oil']
        oil_volume=round(oil_volume0*(tmax))

        # Plume 'before' state initialization
        plume_state_b = np.array([m0, u0*m0, v0*m0, w0*m0, c0*m0, x0, y0, z0, T0*m0, S0*m0])

        Flag1 = True
        Flag2 = True

        Fd2=p['v_0']**2/(2*p['g1']*p['b'])


        outdata = np.array([0., m0, u0, p['v_0'], c0, p['rho'],p['rhoa_0'], p['h'], p['b'], x0, y0, z0])
        paramdata = np.array([0., p['alpha'], proj_vel(p), p['v_0'], p['rhoa_0'], Qs, Qf, Qe, p['v_phi'], p['g1'],Fd2 ])


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # TIME-EVOLUTION STARTS

        for t in tqdm_green(range(0,tmax)):

            if t < cyl:
            # the cylinder is not yet released
                outdata1=np.array([(t+1)*dt/60., m0, u0, p['v_0'], c0, p['rho'],p['rhoa_0'], p['h'], p['b'], x0, y0, z0])

            else:
            # the cylinder is released

                # UPDATE PLUME : NEW STATE = BEFORE STATE + STATE VARIATION

                plume_state_n = plume_state_b + RK4(model,p,plume_state_b,dt)

                # Retrieve plume state variables

                m = plume_state_n[0]
                u,v,w = plume_state_n[1]/plume_state_n[0], plume_state_n[2]/plume_state_n[0], plume_state_n[3]/plume_state_n[0]
                c = plume_state_n[4]/plume_state_n[0]
                x,y,z = plume_state_n[5], plume_state_n[6], plume_state_n[7]
                T,S = plume_state_n[8]/plume_state_n[0], plume_state_n[9]/plume_state_n[0]


                # Update ambient ocean data at the cylinder depth 

                if z < 0 :
                    p['Ta'],p['Sa'] = float(f_thetao(z)), float(f_so(z))
                    p['rhoa']=  float(f_rhoa(z))
                    p['ua']=float(f_uo(z))
                    p['va']=float(f_vo(z))
                else :
                    break


                # Update all remaining parameters

                p['c'] = c
                p['rho_oil'] = rho_oil_0 * (1 - p['c_T'] * (T - T_oil_0))
                p['rho_w'] = gsw.density.rho(S,T,1)
                p['rho'] =  p['rho_oil']* p['rho_w'] / (p['rho_oil']*(1-c) + p['rho_w']*c)
                p['g1']= reduced_g(p)

                p['u']= u
                p['v']= v
                p['alpha']=entrain_coeff_yapa(p)

                p['v_0b']=p['v_0']
                p['v_0'] = np.sqrt(u**2 + v**2 + w**2)

                p['ds'] = np.sqrt((x-plume_state_b[5])**2 +(y-plume_state_b[6])**2+(z-plume_state_b[7])**2)
                p['h']= np.abs(p['v_0']/p['v_0b'] * p['h'])

                p['bb']=p['b']
                p['b']=np.sqrt(m/(p['rho']*np.pi*p['h']))

                p['v_thetab']=p['v_theta']
                p['v_theta']=np.arctan2(v,u)
                p['v_phib']=p['v_phi']
                p['v_phi']=np.arcsin(w/p['v_0'])

                Fd2=p['v_0']**2/(2*p['g1']*p['b'])

                Qs = shear_entrain_yapa(p)
                Qf = forced_entrain_yapa(p)

                if p['total_entrain'] == 0:
                    Qe = max(Qs,Qf)
                elif p['total_entrain'] == 1:
                    Qe = Qs + Qf


                # Update the 'before' state

                plume_state_b = plume_state_n

                # When density is equal to ocean density, find neutral buoyancy
                if p['g1'] <= 0. and Flag1 :   #0.215 for max
                    Flag1=False
                    neu_buoy=z
                    print('Neutral buoyancy at depth {} m and time {} mins.'.format(z,(t+1)*dt/60 ))

                # When velocity intensity lowers below a threshold, find maximum height
                if (p['alpha'] < -5. or w<0.001) and Flag2 :
                    Flag2 = False
                    max_height=z
                    print('Maximum height at depth {} m and time {} mins.'.format(z,(t+1)*dt/60 ))
                    break   

                # Update parameters file
                
                paramdata1=np.array([(t+1)*dt/60, p['alpha'], proj_vel(p), p['v_0'], p['rhoa'], Qs, Qf, Qe, p['v_phi'],p['g1'], Fd2])
                paramdata=np.vstack([paramdata,paramdata1])

                # Update output plume file
                outdata1=np.array([((t+1))*dt/60, m, u, w, c, p['rho'],p['rhoa'], p['h'], p['b'], x,y,z])
                outdata = np.vstack([outdata, outdata1])

        

        if z < -1:
            surfacing = False
            final_state = 'subsurface'
        else:
            final_state = 'surface'



        # # # PRINT OUTPUT

        plume_data=pd.DataFrame(data=outdata, columns=['Time [min]', 'Mass', 'U', 'W', 'C', 'Density', 'A_Density', 'Tkness', 'Radius', 'x', 'y', 'z' ])
        plume_data.to_csv(rf'{exp_dir}/plumeState.csv', index=False, header=True, float_format='%.8f', sep='\t', mode='w')

        parameters=pd.DataFrame(data=paramdata, columns=['Time [min]', 'alpha', 'va proj', 'v_0', 'rhoa', 'Qs', 'Qf', 'Qe', 'v_phi', 'g1', 'Fd2'])
        parameters.to_csv(rf'{exp_dir}/parameters.csv', index=False, header=True, float_format='%.8f', sep='\t', mode='w')


    compute_and_save_product_summary(exp_dir, runId, numerical_namelist, release_namelist, ambient_namelist)
