'''
GUI for a quick tabular data cleaner (.csv) 
'''
import os
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pandas as pd


class CSVDataCleaner(ctk.CTk):
    
    # APP MAIN
    def __init__(self):
        super().__init__()
        self.title('')
        self.resizable(False, False)
        self.geometry('400x400')
        self.rowconfigure((0,1,2,3,4,5), weight = 1, uniform = 'a') #TODO
        self.columnconfigure((1), weight = 1, uniform = 'a') #TODO
        
        self.df = None # Uploaded dataframe
        
        # WIDGETS
        self.title = ctk.CTkLabel(self, text='Data Cleaner Express')     
        
        self.upload = ctk.CTkButton(self, hover=True, 
                                    text='Upload a .csv file',
                                    command=self.upload)
        self.dropdupes = ctk.CTkButton(self, hover=True, 
                                    text='Drop full duplicate row(s)',
                                    state='disabled',
                                    command=self.dupes)
        self.dropnan = ctk.CTkButton(self, hover=True, 
                                    text='Drop any NaN row(s)',
                                    state='disabled',
                                    command=self.nans)
        self.filesave = ctk.CTkButton(self, hover=True, 
                                    text='Save modified file',
                                    state='disabled',
                                    command=self.save)
        
        self.status = ctk.CTkLabel(self, text='No file loaded')

        # PACK WIDGETS
        self.title.pack(pady=40)
        
        self.upload.pack(pady=10)
        self.dropdupes.pack(pady=10)
        self.dropnan.pack(pady=10)
        self.filesave.pack(pady=10)
        
        self.status.pack(pady=20)

    # FUNCTIONALITY
    
    def upload(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        
        if file_path:
            try:    
                self.df = pd.read_csv(file_path)
                self.status.configure(text=f'''File loaded: 
                                      {os.path.basename(file_path)}''')
                
                self.dropdupes.configure(state='normal')
                self.dropnan.configure(state='normal')
                self.filesave.configure(state='normal')
                
            except Exception as e:
                messagebox.showerror('Upload Error', f'''Could not upload file.\n
                                     Error: {e}''')

    def dupes(self):
        
        if self.df is not None:
            self.df.drop_duplicates(inplace=True)
            messagebox.showinfo('Info', 'Duplicate entries removed')
    
    def nans(self):
        
        if self.df is not None:
            self.df.dropna(inplace=True)
            messagebox.showinfo('Info', 'Missing values removed')
    
    def save(self):
        
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                     filetypes=[("CSV Files", 
                                                                 "*.csv")])
            if file_path:
                try:
                    self.df.to_csv(file_path, index=False)
                    messagebox.showinfo('Info', 
                                        f'File saved at {file_path}')
                    
                except Exception as e:
                    messagebox.showerror('Error', 
                                         'Could not save file:\n Error: {e}')

# RUN APP

if __name__ == "__main__":
    app = CSVDataCleaner()
    app.mainloop()