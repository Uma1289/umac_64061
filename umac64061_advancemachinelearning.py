# -*- coding: utf-8 -*-
"""umac64061_AdvanceMachineLearning

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ASbAkLLDKr8pe-CwBN4qMS-tnPc-OGpt
"""

from numpy.random import seed
seed(123)
from tensorflow.keras.datasets import imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(
    num_words=10000)

from google.colab import drive
drive.mount('/content/drive')

train_data

train_labels[0]

len(train_labels)

len(train_labels)

test_data

test_labels[0]

max([max(sequence) for sequence in test_data])

"""Converting reviews into clear and readable text"""

word_index = imdb.get_word_index()
reverse_word_index = dict(
    [(value, key) for (key, value) in word_index.items()])
decoded_review = " ".join(
    [reverse_word_index.get(i - 3, "?") for i in train_data[0]])

decoded_review

"""Data preparation

Before training the model, we need to process and prepare the data. This step involves cleaning, tokenizing, and converting text into a suitable format for the neural network.
"""

import numpy as np
def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        for j in sequence:
            results[i, j] = 1.
    return results

"""Vectorizing Data

To make textual data usable for machine learning, we convert it into numerical representations. This process ensures that our model can understand and analyze the input effectively.
"""

a_train = vectorize_sequences(train_data)
b_test = vectorize_sequences(test_data)

a_train[0]

b_train = np.asarray(train_labels).astype("float32")
b_test = np.asarray(test_labels).astype("float32")

"""Building the Model Using ReLU and Compiling It

We design a neural network using the ReLU activation function and compile it with appropriate optimization and loss functions. The choice of activation function significantly impacts the model's learning capability.


"""

from tensorflow import keras
from tensorflow.keras import layers
seed(1234)
model = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="rmsprop",
              loss="binary_crossentropy",
              metrics=["accuracy"])

seed(1234)
a_val = a_train[:10000]
partial_a_train = a_train[10000:]
b_val = b_train[:10000]
partial_b_train = b_train[10000:]

seed(1234)
history = model.fit(partial_a_train,
                    partial_b_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(a_val, b_val))

history_dict = history.history
history_dict.keys()

"""Visualizing Model Performance

We plot accuracy and loss graphs to assess how well the model performs during training.


"""

import matplotlib.pyplot as plt
history_dict = history.history
l_values = history_dict["loss"]
val_l_values = history_dict["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict["accuracy"]
val_acc = history_dict["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training accuracy")
plt.plot(epochs, val_acc, "b", label="Validation accuracy")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

"""Understanding the Graphs

The plotted graphs reveal that after a certain number of epochs, the model's ability to generalize declines. This drop is likely due to overfitting, meaning the model learns the training data too well but struggles with new data. To improve performance, we may need to adjust hyperparameters or introduce regularization techniques.

RETRAINING MODEL
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(1234)
model = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])
model.compile(optimizer="rmsprop",
              loss="binary_crossentropy",
              metrics=["accuracy"])
model.fit(a_train, b_train, epochs=4, batch_size=512)


num_features = a_train.shape[1]
num_test_samples = b_test.shape[0]

a_test = np.zeros(shape=(num_test_samples, num_features), dtype=a_train.dtype)
results = model.evaluate(a_test, b_test)

results

"""After retraining, the neural network achieves an accuracy of 69% on the test dataset, with a corresponding loss value of 0.5."""

model.predict(a_test)

"""
Neural Network with One Hidden Layer
"""

seed(1234)
model1 = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model1.compile(optimizer="rmsprop",
              loss="binary_crossentropy",
              metrics=["accuracy"])

a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history1 = model1.fit(partial_a_train,
                    partial_b_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(a_val, b_val))

history_dict = history1.history
history_dict.keys()

import matplotlib.pyplot as plt
history_dict = history1.history
l_values = history_dict["loss"]
val_l_values = history_dict["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "ro", label="Training loss")
plt.plot(epochs, val_l_values, "r", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict["accuracy"]
val_acc = history_dict["val_accuracy"]
plt.plot(epochs, acc, "ro", label="Training accuracy")
plt.plot(epochs, val_acc, "r", label="Validation accuracy")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

np.random.seed(1234)
model1 = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model1.compile(optimizer="rmsprop",
              loss="binary_crossentropy",
              metrics=["accuracy"])
model1.fit(a_train, b_train, epochs=5, batch_size=512)
results1 = model1.evaluate(a_test, b_test)

results1

"""A model with a single hidden layer results in an accuracy of 69% and a loss of 0.5"""

model1.predict(a_test)

"""Neural Network with Three Hidden Layers"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(1234)

model_3 = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model_3.compile(optimizer="rmsprop",
                loss="binary_crossentropy",
                metrics=["accuracy"])



a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]

history3 = model_3.fit(partial_a_train,
                       partial_b_train,
                       epochs=20,
                       batch_size=512,
                       validation_data=(a_val, b_val))

history_dict3 = history3.history
history_dict3.keys()

l_values = history_dict3["loss"]
val_l_values = history_dict3["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "go", label="Training loss")
plt.plot(epochs, val_l_values, "g", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict3["accuracy"]
val_acc = history_dict3["val_accuracy"]
plt.plot(epochs, acc, "go", label="Training acc")
plt.plot(epochs, val_acc, "g", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

np.random.seed(1234)
model_3 = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])


model_3.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model_3.fit(a_train, b_train, epochs=3, batch_size=512)
results_3 = model_3.evaluate(a_test, b_test)

results_3

model_3.predict(a_test)

"""Adding more hidden layers does not always guarantee better performance. However, in this case, the three-layer model shows slightly better accuracy compared to the single-layer version. When designing neural networks, selecting an appropriate number of layers and neurons is crucial for achieving optimal performance

Neural Network with 32 Units per Layer
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(1234)


model_32 = keras.Sequential([
    layers.Dense(32, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])
model_32.compile(optimizer="rmsprop",
                 loss="binary_crossentropy",
                 metrics=["accuracy"])




a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


np.random.seed(1234)
history32 = model_32.fit(partial_a_train,
                         partial_b_train,
                         epochs=20,
                         batch_size=512,
                         validation_data=(a_val, b_val))

history_dict32 = history32.history
history_dict32.keys()

l_values = history_dict32["loss"]
val_l_values = history_dict32["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict32["accuracy"]
val_acc = history_dict32["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

history_32 = model_32.fit(a_train, b_train, epochs=3, batch_size=512)
results_32 = model_32.evaluate(a_test, b_test)
results_32

model_32.predict(a_test)

"""A model with 32 units per hidden layer influences accuracy and computational efficiency. The choice of units per layer should balance complexity and generalization to prevent overfitting or underfitting.with an accuracy of 71% and loss is 0.49

Neural Network with 64 Units per Layer
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)


model_64 = keras.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Dense(64, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])


model_64.compile(optimizer="rmsprop",
                 loss="binary_crossentropy",
                 metrics=["accuracy"])



a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]

np.random.seed(1234)
history64 = model_64.fit(partial_a_train,
                         partial_b_train,
                         epochs=20,
                         batch_size=512,
                         validation_data=(a_val, b_val))

history_dict64 = history64.history
history_dict64.keys()

l_values = history_dict64["loss"]
val_l_values = history_dict64["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict64["accuracy"]
val_acc = history_dict64["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

history_64 = model_64.fit(a_train, b_train, epochs=3, batch_size=512)
results_64 = model_64.evaluate(a_test, b_test)
results_64

model_64.predict(a_test)

"""accuracy is 69% and loss is 0.49

Training the model using a 128-bit configuration.
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)


model_128 = keras.Sequential([
    layers.Dense(128, activation="relu"),
    layers.Dense(128, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model_128.compile(optimizer="rmsprop",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])


a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history128 = model_128.fit(partial_a_train,
                            partial_b_train,
                            epochs=20,
                            batch_size=512,
                            validation_data=(a_val, b_val))

history_dict128 = history128.history
history_dict128.keys()

l_values = history_dict128["loss"]
val_l_values = history_dict128["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict128["accuracy"]
val_acc = history_dict128["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

history_128 = model_128.fit(a_train, b_train, epochs=2, batch_size=512)
results_128 = model_128.evaluate(a_test, b_test)
results_128

model_128.predict(a_test)

"""The model achieved 70% accuracy with a loss of 0.50.

MSE LOSS FUNCTION
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)


model_MSE = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])


model_MSE.compile(optimizer="rmsprop",
                  loss="mse",
                  metrics=["accuracy"])



a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history_model_MSE = model_MSE.fit(partial_a_train,
                                   partial_b_train,
                                   epochs=20,
                                   batch_size=512,
                                   validation_data=(a_val, b_val))

history_dict_MSE = history_model_MSE.history
history_dict_MSE.keys()

import matplotlib.pyplot as plt
l_values = history_dict_MSE["loss"]
val_l_values = history_dict_MSE["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict_MSE["accuracy"]
val_acc = history_dict_MSE["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model_MSE.fit(a_train, b_train, epochs=8, batch_size=512)
results_MSE = model_MSE.evaluate(a_test, b_test)
results_MSE

model_MSE.predict(a_test)

"""*Tanh* Activation Function"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)

model_tanh = keras.Sequential([
    layers.Dense(16, activation="tanh"),
    layers.Dense(16, activation="tanh"),
    layers.Dense(1, activation="sigmoid")
])


model_tanh.compile(optimizer='rmsprop',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])



a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]

history_tanh = model_tanh.fit(partial_a_train,
                               partial_b_train,
                               epochs=20,
                               batch_size=512,
                               validation_data=(a_val, b_val))

history_dict_tanh = history_tanh.history
history_dict_tanh.keys()

l_values = history_dict_tanh["loss"]
val_l_values = history_dict_tanh["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict_tanh["accuracy"]
val_acc = history_dict_tanh["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model_tanh.fit(a_train, b_train, epochs=8, batch_size=512)
results_tanh = model_tanh.evaluate(a_test, b_test)
results_tanh

"""Adam Optimizer Function"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)

model_adam = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])


model_adam.compile(optimizer='adam',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])


a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history_adam = model_adam.fit(partial_a_train,
                               partial_b_train,
                               epochs=20,
                               batch_size=512,
                               validation_data=(a_val, b_val))

history_dict_adam = history_adam.history
history_dict_adam.keys()

l_values = history_dict_adam["loss"]
val_l_values = history_dict_adam["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict_adam["accuracy"]
val_acc = history_dict_adam["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model_adam.fit(a_train, b_train, epochs=4, batch_size=512)
results_adam = model_adam.evaluate(a_test, b_test)
results_adam

"""Regularization"""

from tensorflow.keras import regularizers
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)

model_regularization = keras.Sequential([
    layers.Dense(16, activation="relu", kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(16, activation="relu", kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(1, activation="sigmoid")
])


model_regularization.compile(optimizer="rmsprop",
                             loss="binary_crossentropy",
                             metrics=["accuracy"])




a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history_model_regularization = model_regularization.fit(partial_a_train,
                                                       partial_b_train,
                                                       epochs=20,
                                                       batch_size=512,
                                                       validation_data=(a_val, b_val))


history_dict_regularization = history_model_regularization.history

history_dict_regularization.keys()

l_values = history_dict_regularization["loss"]
val_l_values = history_dict_regularization["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict_regularization["accuracy"]
val_acc = history_dict_regularization["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model_regularization.fit(a_train, b_train, epochs=8, batch_size=512)
results_regularization = model_regularization.evaluate(a_test, b_test)
results_regularization

"""Regularization with Dropout

"""

from tensorflow.keras import regularizers
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(1234)


model_Dropout = keras.Sequential([
    layers.Dense(16, activation="relu"),
    layers.Dropout(0.5),  # Dropout layer with 50% dropout rate
    layers.Dense(16, activation="relu"),
    layers.Dropout(0.5),  # Dropout layer with 50% dropout rate
    layers.Dense(1, activation="sigmoid")
])


model_Dropout.compile(optimizer="rmsprop",
                      loss="binary_crossentropy",
                      metrics=["accuracy"])


a_val = a_train[:10000]
partial_a_train = a_train[10000:]

b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history_model_Dropout = model_Dropout.fit(partial_a_train,
                                           partial_b_train,
                                           epochs=20,
                                           batch_size=512,
                                           validation_data=(a_val, b_val))


history_dict_Dropout = history_model_Dropout.history


history_dict_Dropout.keys()

l_values = history_dict_Dropout["loss"]
val_l_values = history_dict_Dropout["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict_Dropout["accuracy"]
val_acc = history_dict_Dropout["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model_Dropout.fit(a_train, b_train, epochs=8, batch_size=512)
results_Dropout = model_Dropout.evaluate(a_test, b_test)
results_Dropout

"""Training model with hyper tuned parameters

the training process leverages carefully tuned hyperparameters to enhance convergence and generalization, aiming for more robust performance.
"""

from tensorflow.keras import regularizers
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


np.random.seed(1234)

model_Hyper = keras.Sequential([
    layers.Dense(32, activation="relu", kernel_regularizer=regularizers.l2(0.0001)),
    layers.Dropout(0.5),
    layers.Dense(32, activation="relu", kernel_regularizer=regularizers.l2(0.0001)),
    layers.Dropout(0.5),
    layers.Dense(16, activation="relu", kernel_regularizer=regularizers.l2(0.0001)),
    layers.Dropout(0.5),
    layers.Dense(1, activation="sigmoid")
])


model_Hyper.compile(optimizer="rmsprop",
                    loss="mse",
                    metrics=["accuracy"])



a_val = a_train[:10000]
partial_a_train = a_train[10000:]
b_val = b_train[:10000]
partial_b_train = b_train[10000:]


history_model_Hyper = model_Hyper.fit(partial_a_train,
                                       partial_b_train,
                                       epochs=20,
                                       batch_size=512,
                                       validation_data=(a_val, b_val))


history_dict_Hyper = history_model_Hyper.history

history_dict_Hyper.keys()

l_values = history_dict_Hyper["loss"]
val_l_values = history_dict_Hyper["val_loss"]
epochs = range(1, len(l_values) + 1)
plt.plot(epochs, l_values, "bo", label="Training loss")
plt.plot(epochs, val_l_values, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.clf()
acc = history_dict_Hyper["accuracy"]
val_acc = history_dict_Hyper["val_accuracy"]
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model_Hyper.fit(a_train, b_train, epochs=8, batch_size=512)
results_Hyper = model_Hyper.evaluate(a_test, b_test)
results_Hyper

All_Models_Loss= np.array([results_Dropout[0],results_Hyper[0],results_MSE[0],results_regularization[0],results_tanh[0]])*100
All_Models_Loss
All_Models_Accuracy= np.array([results_Dropout[1],results_Hyper[1],results_MSE[1],results_regularization[1],results_tanh[1]])*100
All_Models_Accuracy
Labels=['Model_Dropout','Model_Hyper','Model_MSE','model_regularization','model_tanh']
plt.clf()

"""Compiling

"""

# @title
fig, ax = plt.subplots()
ax.scatter(All_Models_Loss,All_Models_Accuracy)
for i, txt in enumerate(Labels):
    ax.annotate(txt, (All_Models_Loss[i],All_Models_Accuracy[i] ))
plt.title("Summary for Accuracy and Loss of the Model")
plt.ylabel("Accuracy")
plt.xlabel("Loss")

plt.show()

"""Increasing the model's capacity appears to enhance its performance. For example, adding 32 units raised the accuracy from 69% to 71%. Moreover, by applying regularization techniques, the model achieved a 75% accuracy rate, indicating that with the proper methods, it can effectively generalize to unseen data.

Even though improvements in fitting the training data don't always lead directly to higher accuracy, certain configurations—particularly those with 128 units—demonstrated reduced loss values, suggesting a better fit on the training set.

However, when the number of units increased to 128, accuracy dropped from 71% to 49%. This decline implies that while the model may be fitting the training data well, it struggles to generalize to new data when it becomes overly complex. Thus, it is essential to carefully balance model performance and complexity.

Additionally, in several cases, the loss values remained stagnant at 0.5. This plateau may point to issues with the learning rate, optimization strategy, or initial parameter settings. Overall, the model that employed L2 regularization achieved the best results with a 75% accuracy, making it the top-performing architecture at present. Future iterations and further exploration of the model could yield even more promising outcomes.



"""