'''
Test GUI for binary image classification, with tensorflow Keras 
'''
try:
    import imghdr
    import os
    from tkinter import filedialog, messagebox

    import customtkinter as ctk
    import cv2  # pip install opencv-python
    import numpy as np
    import tensorflow as tf
    from matplotlib import pyplot as plt
    from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                         MaxPooling2D)
    from tensorflow.keras.metrics import BinaryAccuracy, Precision, Recall
    from tensorflow.keras.models import Sequential
except:
    print('Check requirements')

    

class CoralClassifier(ctk.CTk):
    
    # Avoid OutOfMemory error by setting GPU Memory Consumption Growth
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        gpus = tf.config.experimental.set_memory_growth(gpu, True)
    
    # APP MAIN
    def __init__(self):
        super().__init__()
        self.title('')
        self.resizable(False, False)
        self.geometry('400x400')
        # Accepted image file formats
        self.formats = ['jpeg', 'jpg', 'bmp', 'png']
        self.data_dir = None
        self.com_model = None
        
        # WIDGETS
        self.app_title = ctk.CTkLabel(self, text='Image classifier')
        self.info1 = ctk.CTkTextbox(self, height=60, width= 320, 
                                    corner_radius=0)
        self.info1.insert("0.0", "Checkbox requirements! (...)")
        
        self.my_directories = ctk.CTkButton(self, hover=True, 
                                    text='Choose a folder',
                                    command=self.load_directories)
        
        self.train_model = ctk.CTkButton(self, hover=True, 
                                    text='Train',
                                    command=self.train)
        
        self.test_model = ctk.CTkButton(self, hover=True,
                                        text='Test',
                                        command=self.classify_image)
        
        self.save_model = ctk.CTkButton(self, hover=True, 
                                    text='Save model',
                                    command=self.save)
        
        self.status = ctk.CTkLabel(self, text='No data')
        
        # PACK WIDGETS
        self.app_title.pack(pady=20)
        self.info1.pack(pady=10)
        self.my_directories.pack(pady=10)
        self.train_model.pack(pady=10)
        self.test_model.pack(pady=10)
        self.save_model.pack(pady=10)
        
        self.status.pack(pady=20)
        
    # FUNCTIONALITY
        
    def load_directories(self):
        '''User input for folder path - containing a binary
        folder structure (e.g. folderA= "cats" & folderB = "dogs")
        '''
        file_path = filedialog.askdirectory()
        
        if file_path:
            try:
                self.data_dir = file_path
                folder_names = os.listdir(file_path)
                self.status.configure(text=f'''Yielding folders: 
                                      {folder_names}''')
            except Exception as e:
                messagebox.showerror('Upload Error', f'...\n{e}')
    
    def train(self):
        
        try:
            from tensorflow.keras.layers import (Conv2D, Dense, Dropout,
                                                 Flatten, MaxPooling2D)
            from tensorflow.keras.metrics import (BinaryAccuracy, Precision,
                                                  Recall)
            from tensorflow.keras.models import Sequential
            
            tf.data.Dataset.list_files
            data = tf.keras.utils.image_dataset_from_directory(self.data_dir)
            
            data_iterator = data.as_numpy_iterator()
            batch = data_iterator.next()
            
            data = data.map(lambda x, y: (x/255, y))
            scaled_iterator = data.as_numpy_iterator()
            batch = scaled_iterator.next()
            
            train_size = int(len(data) * .7)    # what is used to train the dl model
            val_size = int(len(data) * .2) + 1      # used to eval while we are training
            test_size = int(len(data) * .1)         # post training evaluation
            
            train = data.take(train_size)
            val = data.skip(train_size).take(val_size)
            test = data.skip(train_size+val_size).take(test_size)
            
            model = Sequential()
            model.add(Conv2D(16, (3,3), 1, activation='relu', 
                            input_shape=(256,256,3)))
            model.add(MaxPooling2D())

            model.add(Conv2D(32, (3,3), 1, activation='relu'))
            model.add(MaxPooling2D())

            model.add(Conv2D(16, (3,3), 1, activation='relu'))
            model.add(MaxPooling2D())

            model.add(Flatten())
            model.add(Dense(256, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            
            model.compile('adam', loss=tf.losses.BinaryCrossentropy(), 
                            metrics=['accuracy'])
                        
            logdir = 'logs'
            tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
            hist = model.fit(train, epochs=12, validation_data=val, 
                                callbacks=[tensorboard_callback])
            
            pre = Precision()
            re = Recall()
            acc = BinaryAccuracy()
            
            for batch in test.as_numpy_iterator():
                x, y = batch
                yhat = model.predict(x)
                pre.update_state(y, yhat)
                re.update_state(y, yhat)
                acc.update_state(y, yhat)
            
        except Exception:
            messagebox.showerror('Error', 'Something went wrong')
            
        else:
            self.com_model = model
            self.status.configure(text=f'''Training successful\n
                                  Precision: {pre.result().numpy():.3f}, 
                                  Recall: {re.result().numpy():.3f}, 
                                  Accuracy: {acc.result().numpy():.3f}''')
      
    def classify_image(self):
        img_filename = filedialog.askopenfilename()
        img = cv2.imread(img_filename)
        resize = tf.image.resize(img, (256,256))
        yhat = self.com_model.predict(np.expand_dims(resize/255, 0))

        # with binary classification 0 - 0.5 = 0 (coral) 0.51 - 1 = 1 (sand)
        if yhat <= 0.5:
            print(f'Predicted class is 0')
        else:
            print(f'Pedicted class is 1')

    def save(self):
        #from tensorflow.keras.models import load_model
        
        folder_name = filedialog.askdirectory()
        
        if self.com_model is not None:
            self.com_model.save(os.path.join(folder_name, 'modelname.keras')) # TODO
        

# RUN APP

if __name__ == "__main__":
    app = CoralClassifier()
    app.mainloop()