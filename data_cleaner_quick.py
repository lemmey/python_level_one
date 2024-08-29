'''Summary:
Data cleaner. Quick & dirty for .csv files only.
 
App takes user input of a .csv file, 
removes faulty/duplicate entries 
and saves a 'clean' copy as .csv in the same data folder.
'''
# Packages
import os
from pathlib import Path

import pandas as pd

os.chdir(Path(__file__).parent)

def clean_csv(filename: str, saved_as: str) -> None:
    """Transforms .csv file into pd dataframe and removes Null 
    values and entries matching the header row.

    Args:
        filename (str): filename of input data
        saved_as (str): filename of clean output data file
    """
    DATA_DIR = Path(__file__).parent    #/ "data_folder"
    
    dataframe = pd.read_csv(DATA_DIR/filename)
    
    df_clean = dataframe.copy()

    df_clean.drop_duplicates(inplace=True)

    df_clean.dropna(inplace=True)
    
    df_clean.to_csv('my_data_clean.csv', index= False, header=True)
    
    print(f'''The cleaned dataset was saved as {saved_as}.
    {dataframe.shape[0] - df_clean.shape[0]} faulty rows where removed from {filename}.''')
    

# MAIN
def main():
    in_data, out_data = input('''Please enter the filename.csv and the output
    filename of the clean file separated by a space\n>''')
    
    clean_csv(in_data, out_data)

# RUN
if __name__ == '__main__':
    main()