# -*- coding: utf-8 -*-
"""lab4-409.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15NTSVFx5R8AIuMT54SfP1aS4qS5JjxjD

This code uses the labelled data to train a NN model By Milad Hafezi
"""

import os
root_path = os.path.realpath(os.path.join(os.getcwd()))
load_path = root_path + '/LabelledData/'
os.chdir('/content/LabelledData/')

"""DNN model
Starts Here

"""

import os
os.chdir('/content/')

from __future__ import print_function
import matplotlib.pyplot as plt
from  sklearn.preprocessing import OneHotEncoder
import seaborn as sns
import Lab4Functions_Colab as l4f

""" Importing Data"""
data= l4f.import_data()

""" Preparing data"""

data_train=data[data['id']>2]   # the number participents to be taken as training set
data_test=data[data['id']<=2]  # test set any participant # more than 1
data_train=data_train.reset_index(drop=True)
data_test=data_test.reset_index(drop=True)

plt.figure()

sns.countplot(x='activity',
              data=data,
              order=data.activity.value_counts().index);
plt.title('data per activity')





plt.figure()
sns.countplot(x='id',
              data=data,
              palette=[sns.color_palette()[0]],
              order=data.id.value_counts().index);

plt.title('data per user')

TIME_STEPS= 100
STEP=20

X_train,y_train=l4f.create_dataset(
    data_train[['x','y','z']],
    data_train.activity,
    TIME_STEPS,
    STEP
    )

X_test,y_test=l4f.create_dataset(
    data_test[['x','y','z']],
    data_test.activity,
    TIME_STEPS,
    STEP
    )

enc=OneHotEncoder(handle_unknown='ignore', sparse=False)

enc=enc.fit(y_train)


y_train=enc.transform(y_train)
y_test=enc.transform(y_test)

# DNN

model=l4f.create_model(X_train, y_train)


history=model.fit(
    X_train, y_train,
    epochs=3,    # make sure it is more than 1"""
    validation_split=0.1
    )


plt.figure()
plt.plot(history.history['acc'], label='train')
plt.plot(history.history['val_acc'], label='test')
plt.ylabel('accuracy[%]')
plt.xlabel('Epoch[%]')
plt.legend();

accuracy=model.evaluate(X_test,y_test);
y_pred=enc.inverse_transform(model.predict(X_test))

l4f.plot_cm(
    enc.inverse_transform(y_test),
    y_pred,
    enc.categories_[0])


model.save('my_model.keras')

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as sps



column_names = [
   'x',
   'y',
   'z',
   't',
   'activity'
 ]


df= pd.read_csv('LabelledData (1).csv')
time=df.t/1000

fig,ax=plt.subplots()
plt.title('Labelled Data')

ax.plot(time,df.x)
ax.plot(time,df.y)
ax.plot(time,df.z)

ax.set_ylabel('accelations (G)')
ax.set_xlabel('Time (ms)')

ax2=ax.twinx()
ax2.plot(time,df.activity,color='black')

sfreq=1000/np.mean(np.diff(df.t))



stepdata=df.loc[(df.activity=='Running')|(df.activity == 'Walking')]

stepdata=stepdata.reset_index(drop=True)

stepdata_time=stepdata.t/1000

plt.figure()
plt.plot(stepdata_time,stepdata.x)
plt.plot(stepdata_time,stepdata.y)
plt.plot(stepdata_time,stepdata.z)




"""filteration"""

low_pass=3
low_pass_ratio=low_pass/(sfreq/2)

b2,a2=sps.butter(4,low_pass_ratio,btype='lowpass')

xfilt=sps.filtfilt(b2,a2,stepdata.x)
yfilt=sps.filtfilt(b2,a2,stepdata.y)
zfilt=sps.filtfilt(b2,a2,stepdata.z)



xfilt_peaks,_=sps.find_peaks(xfilt)
yfilt_peaks,_=sps.find_peaks(yfilt)

len(xfilt_peaks)



plt.figure()

plt.plot(stepdata_time,xfilt)
plt.plot(stepdata_time[xfilt_peaks],xfilt[xfilt_peaks],'x',color='g')