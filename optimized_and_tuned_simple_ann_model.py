# -*- coding: utf-8 -*-
"""Optimized_and_Tuned_simple_ANN_Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QVo1OaACMGxG8l4eeuBPJXJer0dNmb5D
"""

#Importing required libraries
import tensorflow as tf
from keras.utils import np_utils
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import datasets
import matplotlib.pyplot as plt

import os
import pandas as pd

from keras.utils import to_categorical
from keras.wrappers.scikit_learn import KerasClassifier

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras import optimizers
from keras.callbacks import History

from sklearn.model_selection import RandomizedSearchCV

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

#Test Train Split
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
print(x_train.shape)
print(x_test.shape)
#plt.imshow(X_train[1170])
#plt.show()

input_dim=x_train.shape[1]
print(input_dim)

# Build Model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras import optimizers

# Function to create model, required for KerasClassifier
def create_model(activation='relu',
                 optimizer='adam'):
    
    # Create model
    model = Sequential()
    # Input
    model.add(Flatten())
    # Hidden
    model.add(Dense(128, activation=activation))
    # Output
    model.add(Dense(10,activation='softmax'))
    
    # Compile model
    model.compile(loss='categorical_crossentropy', 
                  optimizer=optimizer, 
                  metrics=['accuracy'])
    return model

# Create model using Keras Claasifier
kmodel = KerasClassifier(build_fn=create_model)
kmodel.fit(x_train, y_train, epochs=5)

# Specify Hyperparameters and Model Design Components
activation =  ['relu', 'elu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']
optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
epochs = [10,20,30,40,50]
batch_size = [1024,2048]
param_dist = dict (activation=activation,
                   optimizer=optimizer,
                   epochs=epochs,
                   batch_size=batch_size)

# Perform Randomized search
n_iter_search = 10
random_search = RandomizedSearchCV(estimator=kmodel, 
                                   param_distributions=param_dist,
                                   n_iter=n_iter_search,
                                   n_jobs=1, cv=3,
                                   scoring='accuracy')
random_search.fit(x_test, y_test)

# Show results
print("Best: %f using %s" % (random_search.best_score_, random_search.best_params_))
means = random_search.cv_results_['mean_test_score']
stds = random_search.cv_results_['std_test_score']
params = random_search.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

# Choose best Optimized value for the parameters previously defined
a=random_search.best_params_
epo=a.get('epochs')
act=a.get('activation')
bat_sz=a.get('batch_size')
opt=a.get('optimizer')

# Create a simple Model with the best Optimized values
model=Sequential()
model.add(Flatten())
model.add(Dense(128,activation=act))
model.add(Dense(10,activation='softmax'))
model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=epo)

pd.DataFrame(model.history.history).plot()
plt.show()

from matplotlib import pyplot

# plot loss during training
pyplot.subplot(211)
pyplot.title('Loss')
pyplot.plot(model.history.history['loss'], label='train')
#pyplot.plot(model.history.history['val_loss'], label='test')
pyplot.legend()

# plot accuracy during training
pyplot.subplot(212)
pyplot.title('Accuracy')
pyplot.plot(model.history.history['accuracy'], label='train')
#pyplot.plot(model.history.history['val_accuracy'], label='test')
pyplot.legend()
pyplot.show()

# Compute Validation Loss and Accuracy
val_loss,val_acc=model.evaluate(x_test,y_test)
print(val_loss,val_acc)

# Save the model for future use
model.save("model_name.model")

# To use this model
new_model_testing=tf.keras.models.load_model("model_name.model")

# Make prediction using  model
prediction=model.predict(x_test)

# Print the list of predictions
import numpy as np
# this list gives all predictions made
list2=[]

for i in prediction:
    list2.append(np.argmax(i))
    
print(list2)

# Print the required Metrics
# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(y_test, list2)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(y_test, list2,average='weighted')
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(y_test, list2,average='weighted')
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(y_test, list2,average='weighted')
print('F1 score: %f' % f1)
# confusion matrix
matrix = confusion_matrix(y_test, list2)
print(matrix)