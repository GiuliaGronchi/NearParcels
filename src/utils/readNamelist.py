"""
@author: msalinas
@email: mario.salinas@cmcc.it

Set of functions to read yaml namelists
"""

import yaml
import munch
from src.utils.pathDefinition import get_path


def read_yaml_as_munch(namelist_path):
    return munch.munchify(yaml.load(open(namelist_path).read(), Loader=yaml.BaseLoader))


def read_constants(UWORM1_ROOT='.'):
    """
    Add something here Giulia
    """
    # Namelist directory path
    namelistDir = get_path(UWORM1_ROOT=UWORM1_ROOT, dirname='namelist')

    # NaturalConstants namelist file
    constants = read_yaml_as_munch(f'{namelistDir}/NaturalConstants.yaml')

    # Constants values from the name list in array-like
    for variable in constants.keys():
        constants[variable] = float(constants[variable])
    return constants


def read_staticPaths(UWORM1_ROOT='.'):
    """
    Add something here Giulia
    """
    # Namelist directory path
    namelistDir = get_path(UWORM1_ROOT=UWORM1_ROOT, dirname='namelist')

    # NaturalConstants namelist file
    paths = read_yaml_as_munch(f'{namelistDir}/StaticPaths.yaml')

    # Constants values from the name list in array-like
    for variable in paths.keys():
        paths[variable] = paths[variable]
    return paths


def read_namelist(file_name, template='Release', UWORM1_ROOT='.'):
    """
    Function that reads an input namelist and returns it as a dictionary (Munch) object.

    Parameters:
        file_name: filename of the namelist to be read
        template : string that identifies the template. Can be 'NumericalSimulation' or 'Release'
        UWORM1_ROOT: root directory of UWORM-1

    Returns:
        namelist in dictionary format
    """
    # Namelists directory path
    namelistDir = get_path(UWORM1_ROOT=UWORM1_ROOT, dirname='namelist')

    # Template namelist file
    default = read_default_namelist(namelistDir, template=template)

    # Custom namelist file (actual)
    custom = read_yaml_as_munch(f'{namelistDir}/{file_name}.yaml')

    namelist = {}

    # Validate namelist file values (custom / template)
    for key in default.keys():
        namelist[key] = get_values(custom.get(key), default[key], key)

    namelist = munch.munchify(namelist)

    return namelist


def _eval(_custom):
    try:
        # for common data type int, str, float, division and also numpy expressions
        return eval(_custom) if _custom != 'eval' else _custom
    except (NameError, SyntaxError):
        res = ''
        # comma-separated tuples
        if ',' in _custom:
            res = [x.strip() for x in _custom.split(',')]
        else:
            res = _custom
        return res


def get_default_dict_values(in_dict):
    output = {}
    for key in in_dict.keys():
        dval = in_dict[key]
        output[key] = get_default_dict_values(dval) if isinstance(dval, dict) else _eval(dval)
    return output


def get_values(custom, default, in_key):
    result = default

    if custom is not None:
        if isinstance(custom, str):
            if len(custom):
                result = _eval(custom)
        elif isinstance(custom, dict):
            output = {}
            for key in default.keys():
                # try:
                cval = custom[key] if key in custom else None
                dval = default[key]# if key in custom else None
                output[key] = get_values(cval, dval, key)
                # except Exception as e:
                #     raise(f'\t\t\t')
            result = output
        else:
            print('==========')
            print(f'[ERROR] Wrong input type for item {in_key}:')
            print(custom)
            print('==========')
    else:
        result = get_default_dict_values(default) if isinstance(default, dict) else _eval(default)

    return result


def read_default_namelist(namelistDir, template='Release'):
    """
    Function that reads the tamplate_* namelist

    Parameters:
        namelistDir: directory containing the template
        template : string that identifies the template. Can be 'NumericalSimulation' or 'Release'

    Returns:
        namelist in dictionary format
    """
    default_file = namelistDir + f'/template_{template}.yaml'
    default = read_yaml_as_munch(default_file)
    return default


def read_simulation_namelists(UWORM1_ROOT='.'):
    # Read namelist
    fname = 'Ambient'
    ambient_namelist = read_namelist(fname, UWORM1_ROOT=UWORM1_ROOT, template=fname)
    fname = 'NumericalSimulation'
    numerical_namelist = read_namelist(fname, UWORM1_ROOT=UWORM1_ROOT, template=fname)
    fname = 'Release'
    release_namelist = read_namelist(fname, UWORM1_ROOT=UWORM1_ROOT, template=fname)
    fname = 'Render'
    render_namelist = read_namelist(fname, UWORM1_ROOT=UWORM1_ROOT, template=fname)
    # read constants and paths
    constants = read_constants(UWORM1_ROOT=UWORM1_ROOT)
    static_paths = read_staticPaths(UWORM1_ROOT=UWORM1_ROOT)

    return ambient_namelist, numerical_namelist, release_namelist, render_namelist, constants, static_paths

