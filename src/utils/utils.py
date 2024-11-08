"""
@author: msalinas
@email: mario.salinas@cmcc.it

Set of functions of general utility
"""
import sys
from datetime import datetime

from tqdm import tqdm


def dict_to_lists(indict, prev_k='', prefix=''):
    """
    Function that returns
        - the keys in the input dictionary as list of strings
        - the list of values

    It works also for nested dictionaries. Usage example below:

        >>> indict = {'a': 1, 'b':{'b1':1, 'b2':2}}
        >>> key_list, val_list = dict_to_lists(indict)
        >>> print(key_list)
        >>> ['a', 'b_b1', 'b_b2']
        >>> print(val_list)
        >>> [1, 1, 2]

    """
    out_klist = []
    out_vlist = []
    str_sep = '_'
    curr_k_f = lambda k_: k_ if len(prev_k) == 0 else prev_k+k_
    for k, v in indict.items():
        curr_k = curr_k_f(k)
        subkd, subvd = dict_to_lists(v, prev_k=curr_k+str_sep, prefix=prefix) if isinstance(v, dict) else ([prefix+curr_k], [v])
        out_klist += subkd
        out_vlist += subvd

    return out_klist, out_vlist


def get_ntime(fmt='%Y%m%dT%H:%M:%SZ'):
    """
    Get the current time as a string in desired format.
    """
    return datetime.now().strftime(fmt)


def print_ntime(print_msg=''):
    print(f'[{get_ntime(fmt="%Y-%m-%d %H:%M:%S")}] {print_msg}')

def tqdm_green(in_iterable):
    return tqdm(in_iterable, colour='GREEN', file=sys.stdout)