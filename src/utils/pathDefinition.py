def get_path(UWORM1_ROOT='.', dirname="namelist"):
    mod_ = dirname.lower()

    if mod_ == 'namelist':
        return f'{UWORM1_ROOT}/namelist/'
    else:
        print(f'ERROR in get_path. Unrecognized module: {dirname}')
