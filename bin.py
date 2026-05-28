# =========================================
# WEEK 1
# =========================================

# Q1 Smart Home Lighting System

from datetime import datetime

people = int(input("Enter Number of People : "))
hour = datetime.now().hour

if people == 0:
    print("Lights OFF")
elif hour >= 23 or hour < 6:
    print("Dim Lights")
elif 6 <= hour < 18:
    print("Day Mode")
else:
    print("Bright Lights")


# -----------------------------------------


# Q2 MP Neuron from Scratch

import pandas as pd

data = pd.read_csv("data.csv")

x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

split = int(0.7 * len(x))

x_train = x[:split]
x_test = x[split:]

y_train = y[:split]
y_test = y[split:]

threshold = 50

correct = 0

for i in range(len(x_test)):
    total = sum(x_test[i])
    if total >= threshold:
        pred = 1
    else:
        pred = 0
    if pred == y_test[i]:
        correct += 1
accuracy = (correct / len(x_test)) * 100
print("Accuracy =", accuracy)


# -----------------------------------------


# Q3 Weighted Perceptron from Scratch

inputs = [2, 3, 1]
weights = [1, 2, 1]
bias = 0
total = 0
for i in range(len(inputs)):
    total += inputs[i] * weights[i]
total += bias
if total >= 0:
    print(1)
else:
    print(0)


# -----------------------------------------


# Q4 AND OR Gate using Perceptron
def gate(x1, x2, w1, w2, b):
    total = x1 * w1 + x2 * w2 + b
    if total >= 0:
        return 1
    return 0


print("AND Gate")

print(gate(0, 0, 1, 1, -1.5))
print(gate(0, 1, 1, 1, -1.5))
print(gate(1, 0, 1, 1, -1.5))
print(gate(1, 1, 1, 1, -1.5))

print("OR Gate")

print(gate(0, 0, 1, 1, -0.5))
print(gate(0, 1, 1, 1, -0.5))
print(gate(1, 0, 1, 1, -0.5))
print(gate(1, 1, 1, 1, -0.5))


# -----------------------------------------


# Q5 XOR Learning Rule

x = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]
w1 = 0
w2 = 0
b = 0

lr = 0.1
for i in range(10):
    for j in range(4):
        total = x[j][0] * w1 + x[j][1] * w2 + b
        if total >= 0:
            pred = 1
        else:
            pred = 0
        error = y[j] - pred

        w1 += lr * error * x[j][0]
        w2 += lr * error * x[j][1]
        b += lr * error

print("Weights =", w1, w2)
print("Cannot Solve XOR Using Single Perceptron")


# -----------------------------------------


# Q6 Normalization from Scratch

data = [10, 20, 30, 40, 50]
min_val = min(data)
max_val = max(data)
normalized = []
for x in data:
    value = (x - min_val) / (max_val - min_val)
    normalized.append(value)
print(normalized)


# =========================================
# WEEK 2
# =========================================

# Q1 Sigmoid Neuron from Scratch

import math

inputs = [20, 50, 3]
weights = [0.1, 0.2, 0.3]
bias = 0
total = 0
for i in range(len(inputs)):
    total += inputs[i] * weights[i]
total += bias
output = 1 / (1 + math.exp(-total))
print(output)


# -----------------------------------------


# Q2 Raw vs Normalized Data

data = [1000, 2000, 3000, 4000]
min_val = min(data)
max_val = max(data)
print("Normalized Data")
for x in data:
    norm = (x - min_val) / (max_val - min_val)
    print(norm)


# -----------------------------------------


# Q3 XOR using Sigmoid Neuron

import math

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
for x in inputs:
    total = x[0] + x[1] - 0.5
    output = 1 / (1 + math.exp(-total))
    print(output)

print("Cannot Solve XOR Exactly")


# =========================================
# WEEK 3
# =========================================

# Q1 Multi Layer Perceptron from Scratch

import pandas as pd
import random
import math

data = pd.read_csv("data.csv")

x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

split = int(0.7 * len(x))

x_train = x[:split]
x_test = x[split:]

y_train = y[:split]
y_test = y[split:]

weights = []

for i in range(len(x_train[0])):
    weights.append(random.random())
bias = random.random()
lr = 0.01

for epoch in range(10):
    for i in range(len(x_train)):
        total = 0
        for j in range(len(weights)):
            total += x_train[i][j] * weights[j]
        total += bias
        output = 1 / (1 + math.exp(-total))
        error = y_train[i] - output
        for j in range(len(weights)):
            weights[j] += lr * error * x_train[i][j]
        bias += lr * error

correct = 0
for i in range(len(x_test)):
    total = 0
    for j in range(len(weights)):
        total += x_test[i][j] * weights[j]
    total += bias
    output = 1 / (1 + math.exp(-total))
    if output >= 0.5:
        pred = 1
    else:
        pred = 0
    if pred == y_test[i]:
        correct += 1

accuracy = (correct / len(x_test)) * 100

print("Accuracy =", accuracy)


# -----------------------------------------


# Q2 MLP without TensorFlow

x = [[0, 0], [0, 1], [1, 0], [1, 1]]

w1 = 0.5
w2 = 0.5

b = 0

for i in range(4):
    total = x[i][0] * w1 + x[i][1] * w2 + b
    if total >= 1:
        print(1)
    else:
        print(0)


# -----------------------------------------


# Q3 TensorFlow MLP

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()

model.add(Dense(8, input_dim=4, activation="relu"))

model.add(Dense(3, activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy")

print("TensorFlow MLP Ready")


# -----------------------------------------


# Q4 Activation Functions

from math import exp, tanh

x = 2
relu = max(0, x)
sigmoid = 1 / (1 + exp(-x))
print("ReLU =", relu)
print("Sigmoid =", sigmoid)
print("Tanh =", tanh(x))


# -----------------------------------------


# Q5 Optimizer Comparison

optimizers = ["SGD", "Adam", "RMSprop"]
for x in optimizers:
    print("Optimizer =", x)


# -----------------------------------------


# Q6 Hyperparameter Tuning

layers = [1, 2, 3]
neurons = [32, 64]
for l in layers:
    for n in neurons:
        print("Layers =", l, "Neurons =", n)


# =========================================
# WEEK 4
# =========================================

# Q1 1D Convolution

x = [1.0, 1.1, 1.2, 1.4, 1.7, 1.8, 1.9]
w = [0.5, 0.4, 0.01]
s6 = x[6] * w[0] + x[5] * w[1] + x[4] * w[2]
print("s6 =", s6)


# -----------------------------------------


# Q2 CNN using TensorFlow

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense

model = Sequential()

model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(10, activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy")

print("CNN Ready")


# -----------------------------------------


# Q3 Deep CNN

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D

model = Sequential()
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
model.add(Conv2D(64, (3, 3), activation="relu"))
print("Deep CNN Ready")


# -----------------------------------------


# Q4 Data Augmentation

images = ["img1", "img2"]

for x in images:
    print("Rotated", x)
    print("Zoomed", x)
    print("Flipped", x)


# -----------------------------------------


# Q5 Hyperparameter Tuning

filters = [32, 64]

lr = [0.1, 0.01]

for f in filters:
    for l in lr:
        print("Filters =", f, "Learning Rate =", l)


# -----------------------------------------


# Q6 CNN Architecture Comparison

from sklearn.metrics import classification_report

print("LeNet")
print("AlexNet")
print("ZFNet")
print("VGG16")
print("GoogleNet")

y_true = [0, 1, 1, 0]

y_pred = [0, 1, 0, 0]

print(classification_report(y_true, y_pred))


# -----------------------------------------


# Q7 Object Detection

print("Bounding Box Detection")

print("Object Classification")


# =========================================
# WEEK 5
# =========================================

# Q1 Simple RNN from Scratch

import math

xt = 1

st_prev = 0.5

u = 0.8
w = 0.1
b = 0.2

st = 1 / (1 + math.exp(-(u * xt + w * st_prev + b)))

print(st)


# -----------------------------------------


# Q2 GoogLeNet using TensorFlow

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

model = Sequential()

model.add(Conv2D(32, (1, 1), activation="relu", input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3), activation="relu"))
model.add(Conv2D(32, (5, 5), activation="relu"))
model.add(MaxPooling2D((2, 2)))

print("GoogleNet Ready")


# -----------------------------------------


# Q3 ResNet18 Concept

x = 5
shortcut = x
x = x + 2
output = x + shortcut
print(output)


# -----------------------------------------


# Q4 RNN Sentiment Analysis

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Embedding(5000, 64))
model.add(SimpleRNN(64))
model.add(Dense(2, activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy")

print("RNN Model Ready")


# =========================================
# FINAL TEST QUESTIONS
# =========================================

# Q1 MP Neuron Binary Classification

inputs = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
]

outputs = [0, 0, 0, 1, 0, 1, 1, 1]
threshold = 2
correct = 0
for i in range(len(inputs)):
    total = sum(inputs[i])
    if total >= threshold:
        pred = 1
    else:
        pred = 0
    print(inputs[i], "->", pred)
    if pred == outputs[i]:
        correct += 1

accuracy = (correct / len(inputs)) * 100
print("Accuracy =", accuracy)


# -----------------------------------------


# Q2 Perceptron OR Gate


def step(x):
    if x >= 0:
        return 1
    return 0


def perceptron(x1, x2, w1, w2, b):
    total = x1 * w1 + x2 * w2 + b
    return step(total)


print(perceptron(0, 0, 1, 1, -0.5))
print(perceptron(0, 1, 1, 1, -0.5))
print(perceptron(1, 0, 1, 1, -0.5))
print(perceptron(1, 1, 1, 1, -0.5))


# -----------------------------------------


# Q3 Smart Agriculture System

soil = 20
rain = False
time = 20
if rain == True:
    print("Delay Irrigation")
elif soil < 25:
    print("Irrigation ON")
    duration = 100 - soil
    print("Duration =", duration, "minutes")
else:
    print("No Irrigation")
if time == 20:
    print("Night Irrigation Activated")


# -----------------------------------------


# Q4 MLP from Scratch

import pandas as pd
import random
import math

data = pd.read_csv("data.csv")

x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

split = int(0.7 * len(x))

x_train = x[:split]
x_test = x[split:]

y_train = y[:split]
y_test = y[split:]

weights = []

for i in range(len(x_train[0])):
    weights.append(random.random())
bias = random.random()
lr = 0.01
for epoch in range(10):
    for i in range(len(x_train)):
        total = 0
        for j in range(len(weights)):
            total += x_train[i][j] * weights[j]
        total += bias
        output = 1 / (1 + math.exp(-total))
        error = y_train[i] - output
        for j in range(len(weights)):
            weights[j] += lr * error * x_train[i][j]
        bias += lr * error

print("MLP Training Complete")


# -----------------------------------------


# Q5 CNN using TensorFlow

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

model = Sequential()
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(10, activation="softmax"))
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)
model.fit(x_train, y_train, epochs=5)
loss, accuracy = model.evaluate(x_test, y_test)
print("Accuracy =", accuracy)


# -----------------------------------------


# Q6 Deep CNN Architecture Comparison

from sklearn.metrics import classification_report

models = ["Inception", "ResNet", "DenseNet"]
for x in models:
    print("Model =", x)
y_true = [0, 1, 1, 0]
y_pred = [0, 1, 0, 0]

print(classification_report(y_true, y_pred))
