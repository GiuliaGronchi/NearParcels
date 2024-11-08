import shutil

def copy_namelists(exp_dir, UWORM1_ROOT='.'):
    # UWORM1_ROOT = '.'
    namelists=['Ambient', 'NaturalConstants', 'NumericalSimulation', 'Release']

    for namelist in namelists:
        src = f'{UWORM1_ROOT}/namelist/'+str(namelist)+'.yaml'
        dst = exp_dir + '/LOG/'+str(namelist)+'.yaml'
        
        shutil.copyfile(src, dst)


if __name__ == '__main__':
    copy_namelists()
