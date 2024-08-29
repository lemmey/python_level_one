'''
Pseudo Random Data Generator (pRDG) with pandas.

The script is a framework for a random data generator using pandas dataframe 
for a columnar data table, in which each column describes a separate data group
.

The RDG should be able to generate various data formats e.g. random numerical 
data and be dynamically setup by user input.

If wanted, a .csv file is created as output, containing the randomized input 
datatypes as columns.
'''
# Packages
import logging
import random
from random import choices

import numpy as np
import pandas as pd
from numpy import random

########################

# Develop an unique_series
def unique_col(UI_unique: int):
    """Creates a numpy array of consecutive unique integer values
        from 1 to an user-specified size.
        
    Returns:
        Numpy array
    """
    unique_series = np.arange(1, UI_unique + 1, 1)

    return unique_series


# Develop an integer series
def int_col(UI_int_start: int, UI_int_end: int, UI_unique: int):
    """Creates a numpy array of pseudo random integer values
        specified in range by the user.

    Returns:
        Numpy array
    """
    
    int_series = random.randint(UI_int_start, UI_int_end, UI_unique)
    
    return int_series


# Develop a float series
def flt_col(UI_flt_start: float, UI_flt_end: float, UI_unique: int):
    """Creates a numpy array of pseudo random float values
        specified in range by the user.

    Returns:
        Numpy array
    """
    
    float_series = np.random.uniform(UI_flt_start, UI_flt_end, UI_unique)
    
    return float_series


# Develop a string series
def str_col(UI_str_start: int, UI_str_end: int, UI_unique: int):
    """Based on user input generates a capitalized gibberish string
    of a length within user parameter.

    Args:
        UI_str_start (int): lower limit length
        UI_str_end (int): upper limit length
        
    Returns:
        Numpy array
    """
    import string

    x = random.randint(UI_str_start, UI_str_end)
    imd = [''.join(choices(string.ascii_lowercase, k=x)
                 ).capitalize() for i in range(UI_unique)]
    rnd_str_list = np.array(imd)
        

    return  rnd_str_list


# Add up numpy arrays to a pandas dataframe
def frame_data(size, ints, floats, strings):
    data = {
        'Unique': size,
        'Integer': ints,
        'Decimal': floats,
        'Characters': strings,
    }

    pd_df = pd.DataFrame(data, columns=['Unique', 
                                        'Integer', 
                                        'Decimal',
                                        'Characters'])

    return pd_df


# Optional export 
def exp_csv(filename, df_main):
    df_main.to_csv(filename, index=False)
    logging.info(f'File was saved as {filename}')
    #1 Where was it saved
    

# MAIN
def main():
    logging.basicConfig(filename= "rdg_app.log", level= logging.DEBUG,
                            format= """%(asctime)s - %(filename)s - %(name)s - 
                            %(levelname)s - %(message)s """)
    # logging.debug('This is a debug Message')
    logging.info('This is an info Message')
    # logging.warning('This is a warning Message')
    # logging.error('This is an error Message')
    # logging.critical('This is an error Message')
    
    UI_unique = int(input('Please enter a sample size\n>'))
    
    size = unique_col(UI_unique)
    #2 Do you want to add? (y/n)
    UI_int_start, UI_int_end = input(
        '''Please enter an integer start and a stop value separated by a space
        \n>''').split()
    
    ints = int_col(int(UI_int_start), int(UI_int_end), UI_unique)
    #2.5 Floats rounded by ?
    UI_flt_start, UI_flt_end = input(
        '''Please enter an integer start and a stop value separated by a space
        \n>''').split()
    
    floats = flt_col(float(UI_flt_start), float(UI_flt_end), UI_unique)
    
    UI_str_start, UI_str_end = input(
        '''Please enter an integer start and a stop value separated by a space
        \n>''').split()
    
    strings = str_col(int(UI_str_start), int(UI_str_end), UI_unique)
    
    df_main = frame_data(size, ints, floats, strings)
    
    #3 TODO Add functionality: Choice (Show, export or both) / add index y/n
    
    action = input('''Please enter action (show/export)
                   \n>''')
    
    if action == 'show':
        
        print(df_main)
        
    elif action == 'export':
        
        filename = input('''Please enter a filename.csv
                   \n>''')
        
        exp_csv(filename, df_main)


# RUN
if __name__ == '__main__':
    #4 TODO add user app info()
    #5 TODO bugproof app for invalid/faulty user input
    #6 TODO increase/add usability/app feedback to user
    main()