'''Summary:
Extract unique words and their frequencies from a .txt file
 
Python 3.10.10 64-bit
Juli/2024 
'''
# Packages
import csv
# import os
import re
from pathlib import Path


def word_count(filename, folder, mode, output_name):
    try:
        # Write path to input data into a constant
        DATA_DIR = Path(__file__).parent/folder
        text_raw = open(DATA_DIR/filename, mode='r')
    except:
        print('Folder or filename not found.')
    else:
        print('File loaded successfully.')
    
    text_dict = {}
        
    text_raw_str = text_raw.read().lower().casefold()
    text_str_clean = re.sub(r'[^a-zA-Z\s]', '', text_raw_str)
    text_raw_split = text_str_clean.split()
    
    for word in text_raw_split:
        text_dict.update({word: text_raw_str.count(word)})
    
    sorted_on_count = dict(sorted(text_dict.items(), 
                                  key=lambda item: item[1], 
                                  reverse=True))
    
    text_raw.close()
    
    if mode == 'write':
        try:
            with open(DATA_DIR/output_name, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                writer.writerow(['Word', 'Count'])
                
                for key, value in sorted_on_count.items():
                    freq_gt = 10
                    if len(key) > 3 and value >= freq_gt:
                        counter =+ 1
                        writer.writerow([key, value])
        except:
            print('Something went wrong')
        else:
            print(f'''Your word count file was written as {output_name}, 
                  containing {counter} entries''')


if __name__ == '__main__':
    FOLDER_NAME = input('Enter the data folder name:\n')
    USER_FILENAME = input('Enter the full filename:\n')
    MODE = input('Enter the action (write/show):\n')
    OUTPUT = input('Enter the output (.csv) filename:\n')
    word_count(USER_FILENAME, FOLDER_NAME, MODE, OUTPUT)