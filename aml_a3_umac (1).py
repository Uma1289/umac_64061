# -*- coding: utf-8 -*-
"""AML_A3_UmaC

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z_9UGrT8ctU-vNvt1QA7BWctRsO4kkJt
"""

!wget https://s3.amazonaws.com/keras-datasets/jena_climate_2009_2016.csv.zip
!unzip jena_climate_2009_2016.csv.zip

"""**The analysis of Jena weather dataset data**

"""

import os
fname = os.path.join("jena_climate_2009_2016.csv")
with open(fname) as f:
    data = f.read()

lines_data_data = data.split("\n")
header = lines_data_data[0].split(",")
lines_data_data= lines_data_data[1:]
print(header)
print(len(lines_data_data))

"""**Viewing the data**"""

!pip install numpy

import numpy as np

temperature = np.zeros((len(lines_data_data),))
raw_data = np.zeros((len(lines_data_data), len(header) - 1))
for i, line in enumerate(lines_data_data):
    values = [float(x) for x in line.split(",")[1:]]
    temperature[i] = values[1]
    raw_data[i, :] = values[:]

"""**Temperature time series charting**"""

from matplotlib import pyplot as plt
plt.plot(range(len(temperature)), temperature)

"""**Plotting the temperature data for the first ten days**

"""

plt.plot(range(1250), temperature[:1250])

"""**Determine the sample numbers for each data split**"""

num_training_samples = int(0.2 * len(raw_data))
num_validation_samples = int(0.15 * len(raw_data))
num_test_samples = len(raw_data) - num_training_samples - num_validation_samples
print("num_training_samples:", num_training_samples)
print("num_validation_samples:", num_validation_samples)
print("num_test_samples:", num_test_samples)

"""**Preparing the Data**

Normalization of Data
"""

mean = raw_data[:num_training_samples].mean(axis=0)
raw_data -= mean
std = raw_data[:num_training_samples].std(axis=0)
raw_data /= std
import numpy as np
from tensorflow import keras
initial_sequence = np.arange(10)
dummy_data = keras.utils.timeseries_dataset_from_array(
data=initial_sequence[:-2],
targets=initial_sequence[2:],
sequence_length=4,
batch_size=1,
)
for inputs, targets in dummy_data:
    for i in range(inputs.shape[0]):
        print([int(x) for x in inputs[i]], int(targets[i]))

"""**The development of real-time datasets serves for both training and validating and testing purposes.**"""

sampling_rate = 4
sequence_length = 80
delay = sampling_rate * (sequence_length + 24 - 1)
batch_size = 128

training_dataset = keras.utils.timeseries_dataset_from_array(
raw_data[:-delay],
targets=temperature[delay:],
sampling_rate=sampling_rate,
sequence_length=sequence_length,
shuffle=True,
batch_size=batch_size,
start_index=0,
end_index=num_training_samples)

validation_dataset = keras.utils.timeseries_dataset_from_array(
raw_data[:-delay],
targets=temperature[delay:],
sampling_rate=sampling_rate,
sequence_length=sequence_length,
shuffle=True,
batch_size=batch_size,
start_index=num_training_samples,
end_index=num_training_samples + num_validation_samples)

test_dataset = keras.utils.timeseries_dataset_from_array(
raw_data[:-delay],
targets=temperature[delay:],
sampling_rate=sampling_rate,
sequence_length=sequence_length,
shuffle=True,
batch_size=batch_size,
start_index=num_training_samples + num_validation_samples)

"""**Reviewing the results generated by one of our selected datasets**"""

for samples, targets in training_dataset:
    print("samples shape:", samples.shape)
    print("targets shape:", targets.shape)
    break

"""**A reasonable baseline that isn't machine learning**

Establishing the suitable baseline for MAE calculation.
"""

def evaluate_naive_method(dataset):
    total_abs_err = 0.
    samples_seen = 0
    for samples, targets in dataset:
        preds = samples[:, -1, 1] * std[1] + mean[1]
        total_abs_err += np.sum(np.abs(preds - targets))
        samples_seen += samples.shape[0]
    return total_abs_err / samples_seen
print(f"Validation MAE: {evaluate_naive_method(validation_dataset):.2f}")
print(f"Test MAE: {evaluate_naive_method(test_dataset):.2f}")

"""**We can explore a fundamental machine-learning model at this time.**

**A tightly connected model functions through training as well as assessment procedures.**
"""

from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
# Remove the Flatten layer
# x = layers.Flatten()(inputs)
x = layers.Dense(16, activation="relu")(inputs) # Apply Dense layer directly to the input
#x = layers.Flatten()(x) # Apply Flatten after Dense layer or another suitable layer

# Reshape the output of the Dense layer using Reshape before flattening
# or global average pooling if it is appropriate for your data
x = layers.Reshape((-1,16))(x)  # Reshape to (None, 80*16)
x = layers.Flatten()(x)

outputs = layers.Dense(1)(x)

model = keras.Model(inputs, outputs)
callbacks = [
    keras.callbacks.ModelCheckpoint("jena_dense.keras",
                                    save_best_only=True)
]
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
history = model.fit(training_dataset,
                    epochs=10,
                    validation_data=validation_dataset,
                    callbacks=callbacks)
model = keras.models.load_model("jena_dense.keras") # Load the model with the .keras extension
print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}")

"""**Results**"""

import matplotlib.pyplot as plt
loss = history.history["mae"]
validation_loss = history.history["val_mae"]
epochs = range(1, len(loss) + 1)
plt.figure()
plt.plot(epochs, loss, "bo", label="Training MAE")
plt.plot(epochs, validation_loss, "b", label="Validation MAE")
plt.title("Training and validation MAE")
plt.legend()
plt.show()

"""**A 1D convolutional model served as the main objective for implementation.**"""

inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
x = layers.Conv1D(8, 24, activation="relu")(inputs)
x = layers.MaxPooling1D(2)(x)
x = layers.Conv1D(8, 12, activation="relu")(x)
x = layers.MaxPooling1D(2)(x)
x = layers.Conv1D(8, 6, activation="relu")(x)
x = layers.GlobalAveragePooling1D()(x)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs, outputs)
callbacks = [
    keras.callbacks.ModelCheckpoint("jena_conv.keras", # Change the filepath to end with .keras
                                    save_best_only=True)
                                    # Removed save_format='tf' as it is not supported in older versions of Keras
]
# ... (rest of the code remains the same) ...
#model = keras.models.load_model("jena_conv.keras") # Load the model with the .keras extension
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
history = model.fit(training_dataset,
epochs=10,
validation_data=validation_dataset,
callbacks=callbacks)
model = keras.models.load_model("jena_conv.keras") #Fixed the file name
print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}")

"""**LSTM-Based Model Represents the Initial Recurring Baseline**"""

inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
x = layers.LSTM(16)(inputs)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs, outputs)
callbacks = [
    keras.callbacks.ModelCheckpoint("jena_lstm.keras", # Changed the filepath to jena_lstm.keras
                                    save_best_only=True) # remove save_format argument
]
# The file 'jena_lstm.keras' might not exist initially,
# leading to a FileNotFoundError when trying to load it.
# We only load the model if it exists.
import os
if os.path.exists("jena_lstm.keras"):
    model = keras.models.load_model("jena_lstm.keras")
else:
    print("Model file not found. Training from scratch.")

model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
history = model.fit(training_dataset,
epochs=10,
validation_data=validation_dataset,
callbacks=callbacks)
# Loading the best model which is saved during training
model = keras.models.load_model("jena_lstm.keras")
print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}")

"""**Recurrent neural network detection A NumPy RNN implementation**"""

import numpy as np
timesteps = 50
input_features = 32
output_features = 64
inputs = np.random.random((timesteps, input_features))
state_t = np.zeros((output_features,))
W = np.random.random((output_features, input_features))
U = np.random.random((output_features, output_features))
b = np.random.random((output_features,))
successive_outputs = []
for input_t in inputs:
    output_t = np.tanh(np.dot(W, input_t) + np.dot(U, state_t) + b)
    successive_outputs.append(output_t)
    state_t = output_t
final_output_sequence = np.stack(successive_outputs, axis=0)

"""**The recurrent layers of Keras includes An RNN layer that supports any sequence length**"""

num_features = 14
inputs = keras.Input(shape=(None, num_features))
outputs = layers.SimpleRNN(16)(inputs)

"""**The RNN layer delivers information from only its final step of operation**"""

num_features = 14
steps = 80
inputs = keras.Input(shape=(steps, num_features))
outputs = layers.SimpleRNN(16, return_sequences=False)(inputs)
print(outputs.shape)

"""**The RNN layer generates an entire sequence of output values.**"""

num_features = 14
steps = 80
inputs = keras.Input(shape=(steps, num_features))
outputs = layers.SimpleRNN(16, return_sequences=True)(inputs)
print(outputs.shape)

"""**Stacking tiers for Recurrent neural networks**"""

inputs = keras.Input(shape=(steps, num_features))
x = layers.SimpleRNN(16, return_sequences=True)(inputs)
x = layers.SimpleRNN(16, return_sequences=True)(x)
outputs = layers.SimpleRNN(16)(x)

"""**Researchers extensively use recurrent neural networks while designing overfitting management methodologies for frequent dropout situations to work with a dropout-regularized long short-term memory (LSTM).**"""

inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
x = layers.LSTM(16, recurrent_dropout=0.15)(inputs)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs, outputs)
callbacks = [
    keras.callbacks.ModelCheckpoint("jena_lstm_dropout.keras", # Changed filepath to end with .keras
                                    save_best_only=True)
]
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
history = model.fit(training_dataset,
epochs=30,
validation_data=validation_dataset,
callbacks=callbacks)

"""**The research evaluates training and evaluation of a GRU model with dropout regularization while using recurrent layer stacking.**"""

inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
x = layers.GRU(16, recurrent_dropout=0.2, return_sequences=True)(inputs)
x = layers.GRU(16, recurrent_dropout=0.2)(x)
x = layers.Dropout(0.2 )(x)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs, outputs)
callbacks = [
    keras.callbacks.ModelCheckpoint("jena_stacked_gru_dropout.keras", # Changed the filepath to end with .keras
                                    save_best_only=True)
]
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
history = model.fit(training_dataset,
epochs=30,
validation_data=validation_dataset,
callbacks=callbacks)
model = keras.models.load_model("jena_stacked_gru_dropout.keras") # Changed the file path to have the correct .keras extension
print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}")

"""**Bilateral LSTM training combines RNNs to obtain new approaches in assessment and learning processes.**"""

inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
x = layers.Bidirectional(layers.LSTM(8))(inputs)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs, outputs)
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
history = model.fit(training_dataset,
epochs=10,
validation_data=validation_dataset)