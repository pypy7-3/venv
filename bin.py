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

x = data.iloc[:,:-1].values
y = data.iloc[:,-1].values

split = int(0.7*len(x))

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

accuracy = (correct/len(x_test))*100

print("Accuracy =",accuracy)



# -----------------------------------------


# Q3 Weighted Perceptron from Scratch

inputs = [2,3,1]

weights = [1,2,1]

bias = 0

total = 0

for i in range(len(inputs)):

    total += inputs[i]*weights[i]

total += bias

if total >= 0:

    print(1)

else:

    print(0)



# -----------------------------------------


# Q4 AND OR Gate using Perceptron

def gate(x1,x2,w1,w2,b):

    total = x1*w1 + x2*w2 + b

    if total >= 0:

        return 1

    return 0

print("AND Gate")

print(gate(0,0,1,1,-1.5))
print(gate(0,1,1,1,-1.5))
print(gate(1,0,1,1,-1.5))
print(gate(1,1,1,1,-1.5))

print("OR Gate")

print(gate(0,0,1,1,-0.5))
print(gate(0,1,1,1,-0.5))
print(gate(1,0,1,1,-0.5))
print(gate(1,1,1,1,-0.5))



# -----------------------------------------


# Q5 XOR Learning Rule

x = [[0,0],[0,1],[1,0],[1,1]]

y = [0,1,1,0]

w1 = 0
w2 = 0
b = 0

lr = 0.1

for i in range(10):

    for j in range(4):

        total = x[j][0]*w1 + x[j][1]*w2 + b

        if total >= 0:

            pred = 1

        else:

            pred = 0

        error = y[j] - pred

        w1 += lr*error*x[j][0]
        w2 += lr*error*x[j][1]
        b += lr*error

print("Weights =",w1,w2)

print("Cannot Solve XOR Using Single Perceptron")



# -----------------------------------------


# Q6 Normalization from Scratch

data = [10,20,30,40,50]

min_val = min(data)

max_val = max(data)

normalized = []

for x in data:

    value = (x-min_val)/(max_val-min_val)

    normalized.append(value)

print(normalized)



# =========================================
# WEEK 2
# =========================================

# Q1 Sigmoid Neuron from Scratch

import math

inputs = [20,50,3]

weights = [0.1,0.2,0.3]

bias = 0

total = 0

for i in range(len(inputs)):

    total += inputs[i]*weights[i]

total += bias

output = 1/(1+math.exp(-total))

print(output)



# -----------------------------------------


# Q2 Raw vs Normalized Data

data = [1000,2000,3000,4000]

min_val = min(data)

max_val = max(data)

print("Normalized Data")

for x in data:

    norm = (x-min_val)/(max_val-min_val)

    print(norm)



# -----------------------------------------


# Q3 XOR using Sigmoid Neuron

import math

inputs = [[0,0],[0,1],[1,0],[1,1]]

for x in inputs:

    total = x[0] + x[1] - 0.5

    output = 1/(1+math.exp(-total))

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

x = data.iloc[:,:-1].values
y = data.iloc[:,-1].values

split = int(0.7*len(x))

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

            total += x_train[i][j]*weights[j]

        total += bias

        output = 1/(1+math.exp(-total))

        error = y_train[i] - output

        for j in range(len(weights)):

            weights[j] += lr*error*x_train[i][j]

        bias += lr*error

correct = 0

for i in range(len(x_test)):

    total = 0

    for j in range(len(weights)):

        total += x_test[i][j]*weights[j]

    total += bias

    output = 1/(1+math.exp(-total))

    if output >= 0.5:

        pred = 1

    else:

        pred = 0

    if pred == y_test[i]:

        correct += 1

accuracy = (correct/len(x_test))*100

print("Accuracy =",accuracy)



# -----------------------------------------


# Q2 MLP without TensorFlow

x = [[0,0],[0,1],[1,0],[1,1]]

w1 = 0.5
w2 = 0.5

b = 0

for i in range(4):

    total = x[i][0]*w1 + x[i][1]*w2 + b

    if total >= 1:

        print(1)

    else:

        print(0)



# -----------------------------------------


# Q3 TensorFlow MLP

## MLP using tensorflow::
import tensorflow as tf
from tensorflow.keras import models,layers
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import pandas as pd

(X_train,y_train),(X_test,y_test) = mnist.load_data()

##Normalize -> reshape -> to_categorical
# Normalize
X_train = X_train / 255.0
X_test = X_test / 255.0

# Flatten 28x28 -> 784
X_train = X_train.reshape(-1, 784)
X_test = X_test.reshape(-1, 784)

# One-hot encoding
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

def build_mlp(hidden_layers,activation='relu'):
    model = models.Sequential()
    model.add(layers.Input(shape=(784,)))

    for neuron in hidden_layers:
        model.add(layers.Dense(neuron,activation=activation))
    
    model.add(layers.Dense(10, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

## Different architectures::
architecture = {
    '1_hidden_neuron':[128],
    '2_hidden_neuron':[256,128],
    '3_hidden_neuron':[512,256,128]
}

results = []
for names,hidden_layers in architecture.items():
    print(f'\nTraining:{names}...')
    model = build_mlp(hidden_layers)
    model.fit(
        X_train, y_train_cat,
        epochs = 5,
        batch_size=128,
        validation_split=0.1,
        verbose=1
    )
    loss,acc = model.evaluate(X_test,y_test_cat,verbose=0)
    results.append([
        names,hidden_layers,acc
    ])

result_df = pd.DataFrame(
    results,columns=['Architecture','hidden_layers','Accuracy']
)

print(result_df)




# -----------------------------------------


# Q4 Activation Functions

## MLP using different activations::
activations = ['relu','sigmoid','tanh']

result = []
fixed_layer = [512,128]
for act in activations:
    print(f"Training: {act}....")
    model = build_mlp(hidden_layers=fixed_layer,activation=act)
    model.fit(
        X_train, y_train_cat,
        epochs=5,
        batch_size=128,
        validation_split=0.1,
        verbose=1
    )
    loss,acc = model.evaluate(
        X_test,y_test_cat,verbose=0
    )
    result.append([act,acc])

result_df = pd.DataFrame(result,columns=['Activation','Accuracy'])
print(result_df)



# -----------------------------------------


# Q5 Optimizer Comparison

optimizers = ["SGD","Adam","RMSprop"]

for x in optimizers:

    print("Optimizer =",x)



# -----------------------------------------


# Q6 Hyperparameter Tuning
## Hyper-parameter-tuning::
hidden_layers=[
    [128],
    [256,128],
    [512,256,128]
]

learning_rate = [0.01,0.001]
batch_size = [32,64,128]

results = []

for neurons in hidden_layers:
    for lr in learning_rate:
        for size in batch_size:
            optimizer = tf.keras.optimizers.Adam(
                learning_rate=lr
            )
            print(
                f'Architecture={neurons}',
                f'LR={lr}, Batch={size}'
            )
            model = models.Sequential()
            model.add(layers.Input(shape=(784,)))
            for nn in neurons:
                model.add(layers.Dense(nn,activation='relu'))

            model.add(
                layers.Dense(10,activation='softmax')
            )

            model.compile(
                optimizer=optimizer,
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            model.fit(
                X_train,y_train_cat,
                epochs = 5,
                batch_size=size,
                validation_split=0.1,
                verbose=0
            )
            loss,acc = model.evaluate(
                X_test,y_test_cat,verbose=0
            )

            results.append([neurons,lr,size,acc])



# =========================================
# WEEK 4
# =========================================

# Q1 1D Convolution

x = [1.0,1.1,1.2,1.4,1.7,1.8,1.9]

w = [0.5,0.4,0.01]

s6 = x[6]*w[0] + x[5]*w[1] + x[4]*w[2]

print("s6 =",s6)



# -----------------------------------------


# Q2 CNN using TensorFlow

## simple CNN::
import tensorflow as tf
from tensorflow.keras import models,layers
from tensorflow.keras.datasets import cifar10

(X_train,y_train),(X_test,y_test) = cifar10.load_data()

X_train = X_train/255.0
X_test = X_test/255.0

model = models.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)),
    layers.MaxPool2D((2,2)),
    layers.Flatten(),
    layers.Dense(64,activation='relu'),
    layers.Dense(10,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(X_train,y_train,epochs=2,verbose=1,validation_data=(X_test,y_test))
loss,acc = model.evaluate(X_test,y_test)
print('Accuracy: ',acc*100)



# -----------------------------------------


# Q3 Deep CNN

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D

model = Sequential()

model.add(Conv2D(32,(3,3),
          activation='relu',
          input_shape=(32,32,3)))

model.add(Conv2D(64,(3,3),
          activation='relu'))

print("Deep CNN Ready")



# -----------------------------------------


# Q4 Data Augmentation

import tensorflow as tf
from tensorflow.keras import models,layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import cifar10

# Load Dataset
(X_train,y_train),(X_test,y_test) = cifar10.load_data()

# Normalize
X_train = X_train / 255.0
X_test = X_test / 255.0

# Data Augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Fit augmentation
datagen.fit(X_train)

# CNN Model
model = models.Sequential([

    layers.Conv2D(
        32,
        (3,3),
        activation='relu',
        input_shape=(32,32,3)
    ),
    layers.MaxPool2D((2,2)),

    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPool2D((2,2)),

    layers.Flatten(),

    layers.Dense(128,activation='relu'),

    layers.Dense(10,activation='softmax')
])

# Compile
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train with Data Augmentation
history = model.fit(
    datagen.flow(X_train,y_train,batch_size=32),
    epochs=10,
    validation_data=(X_test,y_test),
    verbose=1
)

# Evaluate
loss,acc = model.evaluate(X_test,y_test)

print(f"Accuracy: {acc*100:.2f}%")



# -----------------------------------------


## Hyperparameter CNN
import tensorflow as tf
from tensorflow.keras import models,layers
from tensorflow.keras.datasets import cifar10

# Load Dataset
(X_train,y_train),(X_test,y_test) = cifar10.load_data()

# Normalize
X_train = X_train / 255.0
X_test = X_test / 255.0

# Hyperparameters
filters_list = [32,64]
kernel_sizes = [(3,3),(5,5)]
learning_rates = [0.001,0.01]
epochs_list = [5,10]

best_acc = 0
best_params = None

# Hyperparameter Tuning
for filters in filters_list:
    for kernel in kernel_sizes:
        for lr in learning_rates:
            for epochs in epochs_list:

                print("\nTesting:")
                print("Filters:",filters)
                print("Kernel:",kernel)
                print("Learning Rate:",lr)
                print("Epochs:",epochs)

                # Model
                model = models.Sequential([

                    layers.Conv2D(
                        filters,
                        kernel,
                        activation='relu',
                        input_shape=(32,32,3)
                    ),

                    layers.MaxPool2D((2,2)),

                    layers.Conv2D(
                        filters*2,
                        kernel,
                        activation='relu'
                    ),

                    layers.MaxPool2D((2,2)),

                    layers.Flatten(),

                    layers.Dense(128,activation='relu'),

                    layers.Dense(10,activation='softmax')
                ])

                # Optimizer
                optimizer = tf.keras.optimizers.Adam(
                    learning_rate=lr
                )

                # Compile
                model.compile(
                    optimizer=optimizer,
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy']
                )

                # Train
                model.fit(
                    X_train,
                    y_train,
                    epochs=epochs,
                    verbose=0
                )

                # Evaluate
                loss,acc = model.evaluate(
                    X_test,
                    y_test,
                    verbose=0
                )

                print("Accuracy:",acc)

                # Save Best Result
                if acc > best_acc:
                    best_acc = acc
                    best_params = (
                        filters,
                        kernel,
                        lr,
                        epochs
                    )

print("\nBest Accuracy:",best_acc)

print("Best Parameters:")
print("Filters:",best_params[0])
print("Kernel Size:",best_params[1])
print("Learning Rate:",best_params[2])
print("Epochs:",best_params[3])


# -----------------------------------------


# Q6 CNN Architecture Comparison

from sklearn.metrics import classification_report

print("LeNet")
print("AlexNet")
print("ZFNet")
print("VGG16")
print("GoogleNet")

y_true = [0,1,1,0]

y_pred = [0,1,0,0]

print(classification_report(y_true,y_pred))



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

st = 1/(1+math.exp(-(u*xt + w*st_prev + b)))

print(st)



# -----------------------------------------


# Q2 GoogLeNet using TensorFlow

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

model = Sequential()

model.add(Conv2D(32,(1,1),
          activation='relu',
          input_shape=(32,32,3)))

model.add(Conv2D(32,(3,3),
          activation='relu'))

model.add(Conv2D(32,(5,5),
          activation='relu'))

model.add(MaxPooling2D((2,2)))

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

model.add(Embedding(5000,64))

model.add(SimpleRNN(64))

model.add(Dense(2,activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy')

print("RNN Model Ready")



# =========================================
# FINAL TEST QUESTIONS
# =========================================

# Q1 MP Neuron Binary Classification

## MP-Neuron::
from sklearn.metrics import accuracy_score
x1 = [0,0,0,0,1,1,1,1]
x2 = [0,0,1,1,0,0,1,1]
x3 = [0,1,0,1,0,1,0,1]
output = [0,0,0,1,0,1,0,1]
dataset = {
    'x1':x1,
    'x2':x2,
    'x3':x3,
    'output':output
}
df = pd.DataFrame(dataset)

X = df.iloc[:,:-1]
y = df.iloc[:,-1]

class MPNeuron:
    def __init__(self):
        self.b = None
    
    def model(self, x):
        return sum(x) >= self.b
    
    def predict(self, X):
        y = []
        for x in X:
            pred = self.model(x)
            y.append(pred)
        return np.array(y) 

    def fit(self, X, y):
        accuracy = {}
        for b in range(X.shape[1]+1):
            self.b = b
            pred = self.predict(X)
            acc = accuracy_score(y,pred)
            accuracy[b] = acc
        best_b = max(accuracy,key=accuracy.get)
        self.b = best_b
        print("Optimal b is: ",self.b)
        print("Maximum Accuracy is: ",accuracy[self.b]*100)

X = X.values
mp_neuron = MPNeuron()
mp_neuron.fit(X,y)


# -----------------------------------------


# Q2 Perceptron OR Gate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

dataset = {
    'x1':[0,0,1,1],
    'x2':[0,1,0,1],
    'Output':[0,1,1,1]
}

df = pd.DataFrame(dataset)

class Perceptron:
    def __init__(self):
        self.w = None
        self.b = None

    def model(self, X):
        return 1 if np.dot(self.w, X) >= self.b else 0

    def predict(self, X):
        y = []

        for x in X:
            pred = self.model(x)
            y.append(pred)

        return np.array(y)

    def fit(self, X, Y, epochs=10, lr=0.1):

        self.w = np.zeros(X.shape[1])
        self.b = 0

        accuracy = {}
        max_accuracy = 0

        for i in range(epochs):

            for x, y in zip(X, Y):

                y_pred = self.model(x)

                if y_pred == 0 and y == 1:
                    self.w += lr * x
                    self.b -= lr

                elif y_pred == 1 and y == 0:
                    self.w -= lr * x
                    self.b += lr

            y_pred = self.predict(X)

            accuracy[i] = accuracy_score(Y, y_pred)

            if accuracy[i] > max_accuracy:
                max_accuracy = accuracy[i]
                chkptw = self.w.copy()
                chkptb = self.b

        self.w = chkptw
        self.b = chkptb

        print("Weights:", self.w)
        print("Bias:", self.b)
        print("Accuracy:", max_accuracy * 100)

        plt.plot(accuracy.values())
        plt.ylim([0,1])
        plt.show()


X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values

perceptron = Perceptron()
perceptron.fit(X, y, 5, 0.1)



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

    print("Duration =",duration,"minutes")

else:

    print("No Irrigation")

if time == 20:

    print("Night Irrigation Activated")



# -----------------------------------------


# Q4 MLP from Scratch

## Multi-Layer Perceptron (MLP) from Scratch

import numpy as np
from sklearn.metrics import accuracy_score

np.random.seed(42)

# -----------------------------
# Synthetic Dataset Generation
# -----------------------------

samples = 100

X = np.column_stack([
    np.random.uniform(0, 1, samples),        # Feature 1
    np.random.uniform(10, 50, samples),      # Feature 2
    np.random.uniform(100, 200, samples),    # Feature 3
    np.random.uniform(1, 10, samples),       # Feature 4
    np.random.uniform(50, 100, samples),     # Feature 5
    np.random.uniform(1000, 5000, samples),  # Feature 6
    np.random.uniform(5, 15, samples),       # Feature 7
    np.random.uniform(20, 80, samples),      # Feature 8
    np.random.uniform(200, 500, samples),    # Feature 9
    np.random.uniform(0, 100, samples)       # Feature 10
])

# Binary Output (0 or 1)
y = ((X[:,0] + X[:,1] + X[:,2]) > 180).astype(int)
y = y.reshape(-1,1)

# -----------------------------
# MLP Class
# -----------------------------

class MLP:
    def __init__(self):
        self.w1 = None
        self.b1 = None
        self.w2 = None
        self.b2 = None

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def predict(self, X):

        # Hidden Layer
        hidden_input = np.dot(X, self.w1) + self.b1
        hidden_output = self.sigmoid(hidden_input)

        # Output Layer
        output_input = np.dot(hidden_output, self.w2) + self.b2
        output = self.sigmoid(output_input)

        return (output >= 0.5).astype(int)

    def fit(self, X, Y, epochs=1000, lr=0.001):

        input_neurons = X.shape[1]   # 10 features
        hidden_neurons = 5
        output_neurons = 1

        # Initialize weights and bias
        self.w1 = np.random.randn(input_neurons, hidden_neurons)
        self.b1 = np.zeros((1, hidden_neurons))

        self.w2 = np.random.randn(hidden_neurons, output_neurons)
        self.b2 = np.zeros((1, output_neurons))

        for epoch in range(epochs):

            # ---------- Forward Propagation ----------

            hidden_input = np.dot(X, self.w1) + self.b1
            hidden_output = self.sigmoid(hidden_input)

            output_input = np.dot(hidden_output, self.w2) + self.b2
            output = self.sigmoid(output_input)

            # ---------- Squared Error Loss ----------

            loss = np.mean((Y - output) ** 2)

            # ---------- Backpropagation ----------

            error = Y - output

            d_output = error * self.sigmoid_derivative(output)

            hidden_error = np.dot(d_output, self.w2.T)
            d_hidden = hidden_error * self.sigmoid_derivative(hidden_output)

            # ---------- Weight Update ----------

            self.w2 += lr * np.dot(hidden_output.T, d_output)
            self.b2 += lr * np.sum(d_output, axis=0, keepdims=True)

            self.w1 += lr * np.dot(X.T, d_hidden)
            self.b1 += lr * np.sum(d_hidden, axis=0, keepdims=True)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")

        pred = self.predict(X)

        acc = accuracy_score(Y, pred)

        print("\nFinal Accuracy:", acc * 100)
        print("Final Squared Error Loss:", loss)


# -----------------------------
# Train Model
# -----------------------------

mlp = MLP()
mlp.fit(X, y)



# -----------------------------------------


# Q5 CNN using TensorFlow

import tensorflow as tf
from tensorflow.keras import models,layers
from tensorflow.keras.datasets import cifar10

# Load Dataset
(X_train,y_train),(X_test,y_test) = cifar10.load_data()

# Normalize
X_train = X_train / 255.0
X_test = X_test / 255.0

# CNN Model
model = models.Sequential([

    # Convolution Layer
    layers.Conv2D(
        32,
        (3,3),
        activation='relu',
        input_shape=(32,32,3)
    ),

    # Pooling Layer
    layers.MaxPool2D((2,2)),

    # Flatten
    layers.Flatten(),

    # Fully Connected Layer
    layers.Dense(64,activation='relu'),

    # Output Layer
    layers.Dense(10,activation='softmax')
])

# Compile Model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    X_train,
    y_train,
    epochs=10,
    validation_data=(X_test,y_test),
    verbose=1
)

# Evaluate
loss,acc = model.evaluate(X_test,y_test)

print(f"Accuracy: {acc*100:.2f}%")



# -----------------------------------------


# Q6 Deep CNN Architecture Comparison

import tensorflow as tf
import time
import pandas as pd

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.applications import (
    ResNet50,
    DenseNet121,
    InceptionV3
)
from tensorflow.keras import models,layers
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)

# Load Dataset
(X_train,y_train),(X_test,y_test) = cifar10.load_data()

# Normalize
X_train = X_train / 255.0
X_test = X_test / 255.0

# Resize images for advanced models
X_train = tf.image.resize(X_train,(75,75))
X_test = tf.image.resize(X_test,(75,75))

results = []

# Dictionary of Models
cnn_models = {
    "ResNet" : ResNet50,
    "DenseNet" : DenseNet121,
    "Inception" : InceptionV3
}

# Train each model
for name, model_class in cnn_models.items():

    print(f"\nTraining {name}...\n")

    # Base Model
    base_model = model_class(
        weights=None,
        include_top=False,
        input_shape=(75,75,3)
    )

    # CNN Model
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(10,activation='softmax')
    ])

    # Compile
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Start Timer
    start = time.time()

    # Train
    model.fit(
        X_train,
        y_train,
        epochs=2,
        batch_size=32,
        verbose=1
    )

    # End Timer
    end = time.time()

    # Prediction
    pred = model.predict(X_test)
    y_pred = pred.argmax(axis=1)

    # Metrics
    accuracy = accuracy_score(y_test,y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        average='weighted'
    )

    recall = recall_score(
        y_test,
        y_pred,
        average='weighted'
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average='weighted'
    )

    execution_time = end - start

    # Store Result
    results.append([
        name,
        accuracy,
        precision,
        recall,
        f1,
        execution_time
    ])

# Final Results Table
df = pd.DataFrame(
    results,
    columns=[
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "Execution Time (sec)"
    ]
)

print("\nFinal Comparison:\n")
print(df)
