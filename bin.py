## Gradient Descent

def function(x, y, z):
    return x**2 + 2*y**2 + 5*z**2


def gradient(x, y, z):
    dx = 2 * x
    dy = 4 * y
    dz = 10 * z
    return dx, dy, dz


lr = 0.1


def gradient_descent(x, y, z):

    i = 0

    while True:

        dx, dy, dz = gradient(x, y, z)

        x = x - lr * dx
        y = y - lr * dy
        z = z - lr * dz

        if i % 10 == 0:
            print(f"Epoch {i}: X={x:.2f} Y={y:.2f} Z={z:.2f}")

        # convergence condition
        if abs(dx) < 1e-5 and abs(dy) < 1e-5 and abs(dz) < 1e-5:
            break

        i += 1

    return x, y, z


x, y, z = 5, 5, 5

x, y, z = gradient_descent(x, y, z)

print(
    f"\nMinimum Value Obtained:"
    f" X={x:.4f} Y={y:.4f} Z={z:.4f}"
    f" and F(X,Y,Z)={function(x,y,z):.4f}"
)

## Find out the standard deviation of N=10 random numbers which are randomly generated between the range of 0 and 1.
import math
import random

N = 10

numbers = [random.uniform(0,1) for _ in range(10)]

mean = sum(numbers)/N 

variance = sum((x-mean)**2 for x in numbers) / N 
std = math.sqrt(variance)

print(numbers)
print(f"Mean = {mean:.4f}")
print(f"Standard deviation = {std:.4f}")

## KNN
import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv('Gastric.csv')

# print(df.shape)

X = df.iloc[:,1:]
y = df.iloc[:,0]

classes = y.unique()

class1 = X[y == classes[0]]
class2 = X[y == classes[1]]


p_values = {}
for col in X.columns:
    mean1 = np.mean(class1[col])
    mean2 = np.mean(class2[col])

    std1 = np.std(class1[col])
    std2 = np.std(class2[col])

    if std1 != std2:
        p_val = abs((mean1-mean2)/(std1-std2))
    else:
        p_val = 0
    
    p_values[col] = p_val

top10 = sorted(
    p_values,
    key=p_values.get,
    reverse=True
)[:10]

print("Top 10 features: ")
print(top10)

X_selected = X[top10]

# convert to numpy::
x_value = X_selected.values
y_value = y.values

## KNN from scratch::
def euclidean(x1,x2):
    return np.sqrt(np.sum((x1-x2)**2))

def knn_predict(X_train, y_train, test_point, k = 5):
    distances = []
    for i in range(len(X_train)):
        dist = euclidean(
            X_train[i],
            test_point
        )
        distances.append((dist,y_train[i]))
    
    distances.sort(key=lambda x:x[0])
    classifier = distances[:k]
    labels = [label for _,label in classifier]
    prediction = Counter(labels).most_common(1)[0][0]
    return prediction

test_point = X_selected.mean().values
print(test_point)
prediction = knn_predict(x_value,y_value,test_point,5)
print(f"Predicted: {prediction}")

## Split the Diabetes dataset into the ratio of 70% and 30%. Calculate mean and standard deviation of the feature BMI by considering the selected 30% data.
import pandas as pd
import numpy as np

df = pd.read_csv('diabetes.csv')

rows,cols = df.shape

seventy_percent = int(rows*0.7)

X_train = df.iloc[:seventy_percent,:]
X_test = df.iloc[seventy_percent:, :]
# X_train = df[:seventy_percent]
# X_test = df[seventy_percent:]

print(X_train.shape)
print(X_test.shape)

print(X_test['BMI'].mean())
print(X_test['BMI'].std())

## Linear Regreesion::
import pandas as pd
import numpy as np

df = pd.read_csv('diabetes.csv')

Y = df['Age']   ## dependent
X = df['BloodPressure'] ## independent

## Y = b1 + b2 X
## b2 = (x-x_mean)(y-y_mean) / (x-x_mean)**2
numerator = np.sum((X-np.mean(X)) * (Y - np.mean(Y)))
denominator = np.sum((X-np.mean(X))**2)

b2 = numerator / denominator
## b1 = y_mean - b2*x_mean
b1 = np.mean(Y) - b2 * np.mean(X)

# age = b1 + b2 * blood_pressure
bp = [34.5,66.5,72.3]
for b in bp:
    age = b1 + b2 * b
    print(f"BP = {b} -> Age = {round(age)}")


## using sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

data=pd.read_csv("data.csv")
X=data.iloc[:,:-1]
y=data.iloc[:,-1]
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.3)


## ID3
id3=DecisionTreeClassifier(criterion='entropy')
id3.fit(x_train,y_train)
pred1=id3.predict(x_test)


## C4.5
c45=DecisionTreeClassifier(criterion='log_loss')
c45.fit(x_train,y_train)
pred2=c45.predict(x_test)

## CART
cart=DecisionTreeClassifier(criterion='gini')
cart.fit(x_train,y_train)
pred3=cart.predict(x_test)

print("ID3")
print("Accuracy =",accuracy_score(y_test,pred1))
print("Precision =",precision_score(y_test,pred1,average='macro'))
print("Recall =",recall_score(y_test,pred1,average='macro'))
print("F1 Score =",f1_score(y_test,pred1,average='macro'))

print("\nC4.5")
print("Accuracy =",accuracy_score(y_test,pred2))
print("Precision =",precision_score(y_test,pred2,average='macro'))
print("Recall =",recall_score(y_test,pred2,average='macro'))
print("F1 Score =",f1_score(y_test,pred2,average='macro'))

print("\nCART")
print("Accuracy =",accuracy_score(y_test,pred3))
print("Precision =",precision_score(y_test,pred3,average='macro'))
print("Recall =",recall_score(y_test,pred3,average='macro'))
print("F1 Score =",f1_score(y_test,pred3,average='macro'))


### Assignment KNN
import math
data=[
([1,2],0),
([2,3],0),
([3,3],0),
([6,5],1),
([7,7],1),
([8,6],1)
]

test = [5,5]
k = 3
distances = []

for x,label in data:
    d = 0
    for i in range(len(x)):
        d = d + (x[i] - test[i]) ** 2
    
    d = math.sqrt(d)
    distances.append((d,label))

distances.sort()
count0 = 0
count1 = 0

for i in range(k):
    label = distances[i]
    if label == 0:
        count0 += 1
    else:
        count1 += 1
if count0 > count1:
    pred = 0
else:
    pred = 1

print("Test Point =",test)
print("Predicted Class =",pred)
print("\nNearest Neighbors")
for i in range(k):
    print(distances[i])

# Linear Regression
import matplotlib.pyplot as plt
x=[1,2,3,4,5]
y=[2,4,6,8,10]
m=0
b=0
lr=0.01
epochs=1000
n=len(x)
## Batch Gradient Descent
for _ in range(epochs):
    dm=0
    db=0
    for i in range(n):
        pred=m*x[i]+b
        dm=dm+(pred-y[i])*x[i]
        db=db+(pred-y[i])
    m=m-lr*(2/n)*dm
    b=b-lr*(2/n)*db
print("Batch Gradient Descent")
print("Slope =",m)
print("Intercept =",b)

pred=[]
for i in range(n):
    pred.append(m*x[i]+b)
## R2 Score
mean=sum(y)/n
ss_total=0
ss_res=0
for i in range(n):
    ss_total=ss_total+(y[i]-mean)**2
    ss_res=ss_res+(y[i]-pred[i])**2

r2=1-(ss_res/ss_total)
print("R2 Score =",r2)

## Graph
plt.scatter(x,y)
plt.plot(x,pred)
plt.show()

## Stochastic Gradient Descent
m=0
b=0
for _ in range(epochs):
    for i in range(n):
        pred=m*x[i]+b

        m=m-lr*(pred-y[i])*x[i]
        b=b-lr*(pred-y[i])

print("\nStochastic Gradient Descent")
print("Slope =",m)
print("Intercept =",b)

## implement naive byes and find TP,TN,acuuracy and precession,recall and f1 score
import pandas as pd

data=pd.read_csv("data.csv")

X=data.iloc[:,:-1].values
y=data.iloc[:,-1].values
split=int(0.7*len(X))

x_train=X[:split]
x_test=X[split:]

y_train=y[:split]
y_test=y[split:]

classes=list(set(y))

def mean(nums):
    return sum(nums)/len(nums)


def std(nums):
    m=mean(nums)
    s=0
    for x in nums:
        s=s+(x-m)**2
    return (s/len(nums))**0.5


def probability(x,m,s):
    e=2.71828
    return (1/((2*3.1416)**0.5*s))*e**(-((x-m)**2)/(2*s*s))


pred=[]

for row in x_test:
    probs={}
    for c in classes:
        rows=[]
        for i in range(len(y_train)):
            if y_train[i]==c:
                rows.append(x_train[i])

        p=len(rows)/len(x_train)

        for j in range(len(row)):
            col=[]
            for r in rows:
                col.append(r[j])

            m=mean(col)
            s=std(col)

            p=p*probability(row[j],m,s)

        probs[c]=p

    best=max(probs,key=probs.get)
    pred.append(best)

tp=0
tn=0
fp=0
fn=0


for i in range(len(y_test)):

    print("Actual =",y_test[i],"Predicted =",pred[i])

    if y_test[i]==1 and pred[i]==1:
        tp+=1

    elif y_test[i]==0 and pred[i]==0:
        tn+=1

    elif y_test[i]==0 and pred[i]==1:
        fp+=1

    elif y_test[i]==1 and pred[i]==0:
        fn+=1
accuracy=(tp+tn)/(tp+tn+fp+fn)
precision=tp/(tp+fp)
recall=tp/(tp+fn)
f1=(2*precision*recall)/(precision+recall)
print("\nAccuracy =",accuracy)
print("Precision =",precision)
print("Recall =",recall)
print("F1 Score =",f1)

# value iteration
m,n = 2,3

V = [[0]*n for _ in range(m)]

g = 0.9
goal = (0,2)

def moves(i,j):
    p = []

    if i+1 < m:p.append((i+1,j))
    if i-1 >= 0:p.append((i-1,j))
    if j+1 < n:p.append((i,j+1))
    if j-1 >= 0:p.append((i,j-1))

    return p

while True:

    new = [r[:] for r in V]

    for i in range(m):

        for j in range(n):

            if (i,j) == goal:
                new[i][j] = 100
                continue

            best = -999

            for x,y in moves(i,j):

                if (x,y) == goal:
                    val = 100
                else:
                    val = g * V[x][y]

                if val > best:
                    best = val

            new[i][j] = best

    if new == V:
        break

    V = new

policy = []

for i in range(m):
    row = []
    for j in range(n):
        if (i,j) == goal:
            row.append('G')
            continue
        best = -999
        move = None
        for x,y in moves(i,j):
            if (x,y) == goal:
                val = 100
            else:
                val = g * V[x][y]
            if val > best:
                best = val
                move = (x,y)
        row.append(move)
    policy.append(row)


print("Value Function: ")

for r in V:
    print(r)

print("Policy:")
for r in policy:
    print(r)

## policy evaluation and improvement
m,n = 2,3

goal = (0,2)

g = 0.9

V = [[0]*n for _ in range(m)]

policy = [[None]*n for _ in range(m)]

def moves(i,j):

    p=[]

    if i+1<m:p.append((i+1,j))
    if i-1>=0:p.append((i-1,j))
    if j+1<n:p.append((i,j+1))
    if j-1>=0:p.append((i,j-1))

    return p


for i in range(m):
    for j in range(n):

        if (i,j)==goal:
            policy[i][j]='G'
        else:
            policy[i][j]=moves(i,j)[0]


while True:

    ## policy evaluation

    while True:

        new=[r[:] for r in V]

        for i in range(m):
            for j in range(n):

                if (i,j)==goal:
                    new[i][j]=100
                    continue

                x,y=policy[i][j]

                if (x,y)==goal:
                    val=100
                else:
                    val=g*V[x][y]

                new[i][j]=val

        if new==V:
            break

        V=new


    ## policy improvement

    stable=True

    for i in range(m):
        for j in range(n):

            if (i,j)==goal:
                continue

            old=policy[i][j]

            best=-999
            move=None

            for x,y in moves(i,j):

                if (x,y)==goal:
                    val=100
                else:
                    val=g*V[x][y]

                if val>best:
                    best=val
                    move=(x,y)

            policy[i][j]=move

            if old!=move:
                stable=False


    if stable:
        break


print("Value Function")

for r in V:
    print(r)

print("\nPolicy")

for r in policy:
    print(r)

## Q learning Algorithm
import random

m,n=2,3

goal=(0,2)

g=0.9
a=0.1
episodes=100

Q={}

def moves(i,j):

    p=[]

    if i+1<m:p.append((i+1,j))
    if i-1>=0:p.append((i-1,j))
    if j+1<n:p.append((i,j+1))
    if j-1>=0:p.append((i,j-1))

    return p


for i in range(m):
    for j in range(n):

        for move in moves(i,j):

            Q[((i,j),move)]=0


for _ in range(episodes):

    state=(0,0)

    while state!=goal:

        actions=moves(state[0],state[1])

        next_state=random.choice(actions)

        if next_state==goal:
            reward=100
        else:
            reward=-1

        future=[]

        for move in moves(next_state[0],next_state[1]):
            future.append(Q[(next_state,move)])

        if future:
            max_q=max(future)
        else:
            max_q=0

        old_q=Q[(state,next_state)]

        Q[(state,next_state)]=old_q+a*(reward+g*max_q-old_q)

        state=next_state


print("Q Table")

for k,v in Q.items():
    print(k,"=",round(v,2))

## Gradient Descent

def function(x, y, z):
    return x**2 + 2*y**2 + 5*z**2

def gradient(x, y, z):
    dx = 2 * x
    dy = 4 * y
    dz = 10 * z
    return dx, dy, dz


lr = 0.1


def gradient_descent(x, y, z):

    i = 0

    while True:

        dx, dy, dz = gradient(x, y, z)

        x = x - lr * dx
        y = y - lr * dy
        z = z - lr * dz

        if i % 10 == 0:
            print(f"Epoch {i}: X={x:.2f} Y={y:.2f} Z={z:.2f}")

        # convergence condition
        if abs(dx) < 1e-5 and abs(dy) < 1e-5 and abs(dz) < 1e-5:
            break

        i += 1

    return x, y, z


x, y, z = 5, 5, 5

x, y, z = gradient_descent(x, y, z)

print(
    f"\nMinimum Value Obtained:"
    f" X={x:.4f} Y={y:.4f} Z={z:.4f}"
    f" and F(X,Y,Z)={function(x,y,z):.4f}"
)

## Find out the standard deviation of N=10 random numbers which are randomly generated between the range of 0 and 1.
import math
import random

N = 10

numbers = [random.uniform(0,1) for _ in range(10)]

mean = sum(numbers)/N 

variance = sum((x-mean)**2 for x in numbers) / N 
std = math.sqrt(variance)

print(numbers)
print(f"Mean = {mean:.4f}")
print(f"Standard deviation = {std:.4f}")

## KNN
import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv('Gastric.csv')

# print(df.shape)

X = df.iloc[:,1:]
y = df.iloc[:,0]

classes = y.unique()

class1 = X[y == classes[0]]
class2 = X[y == classes[1]]


p_values = {}
for col in X.columns:
    mean1 = np.mean(class1[col])
    mean2 = np.mean(class2[col])

    std1 = np.std(class1[col])
    std2 = np.std(class2[col])

    if std1 != std2:
        p_val = abs((mean1-mean2)/(std1-std2))
    else:
        p_val = 0
    
    p_values[col] = p_val

top10 = sorted(
    p_values,
    key=p_values.get,
    reverse=True
)[:10]

print("Top 10 features: ")
print(top10)

X_selected = X[top10]

# convert to numpy::
x_value = X_selected.values
y_value = y.values

## KNN from scratch::
def euclidean(x1,x2):
    return np.sqrt(np.sum((x1-x2)**2))

def knn_predict(X_train, y_train, test_point, k = 5):
    distances = []
    for i in range(len(X_train)):
        dist = euclidean(
            X_train[i],
            test_point
        )
        distances.append((dist,y_train[i]))
    
    distances.sort(key=lambda x:x[0])
    classifier = distances[:k]
    labels = [label for _,label in classifier]
    prediction = Counter(labels).most_common(1)[0][0]
    return prediction

test_point = X_selected.mean().values
print(test_point)
prediction = knn_predict(x_value,y_value,test_point,5)
print(f"Predicted: {prediction}")

## Split the Diabetes dataset into the ratio of 70% and 30%. Calculate mean and standard deviation of the feature BMI by considering the selected 30% data.
import pandas as pd
import numpy as np

df = pd.read_csv('diabetes.csv')

rows,cols = df.shape

seventy_percent = int(rows*0.7)

X_train = df.iloc[:seventy_percent,:]
X_test = df.iloc[seventy_percent:, :]
# X_train = df[:seventy_percent]
# X_test = df[seventy_percent:]

print(X_train.shape)
print(X_test.shape)

print(X_test['BMI'].mean())
print(X_test['BMI'].std())

## Linear Regreesion::
import pandas as pd
import numpy as np

df = pd.read_csv('diabetes.csv')

Y = df['Age']   ## dependent
X = df['BloodPressure'] ## independent

## Y = b1 + b2 X
## b2 = (x-x_mean)(y-y_mean) / (x-x_mean)**2
numerator = np.sum((X-np.mean(X)) * (Y - np.mean(Y)))
denominator = np.sum((X-np.mean(X))**2)

b2 = numerator / denominator
## b1 = y_mean - b2*x_mean
b1 = np.mean(Y) - b2 * np.mean(X)

# age = b1 + b2 * blood_pressure
bp = [34.5,66.5,72.3]
for b in bp:
    age = b1 + b2 * b
    print(f"BP = {b} -> Age = {round(age)}")

## DecisionTreeClassifier::
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ---------- Decision Tree From Scratch ----------
class DT:
    def __init__(self, algo="id3", depth=5):
        self.algo = algo
        self.depth = depth

    def entropy(self, y):
        p = np.bincount(y) / len(y)
        return -sum(i * np.log2(i) for i in p if i > 0)

    def gini(self, y):
        p = np.bincount(y) / len(y)
        return 1 - sum(i**2 for i in p)

    def split(self, X, y, feature, threshold):
        left = X[:, feature] < threshold
        right = ~left
        return X[left], X[right], y[left], y[right]

    def best_split(self, X, y):
        best_score = -1
        best = None

        for f in range(X.shape[1]):
            thresholds = np.unique(X[:, f])

            for t in thresholds:
                X_l, X_r, y_l, y_r = self.split(X, y, f, t)

                if len(y_l) == 0 or len(y_r) == 0:
                    continue

                p_l, p_r = len(y_l)/len(y), len(y_r)/len(y)

                # ID3
                if self.algo == "id3":
                    gain = self.entropy(y) - (
                        p_l*self.entropy(y_l) + p_r*self.entropy(y_r)
                    )
                    score = gain

                # C4.5
                elif self.algo == "c45":
                    gain = self.entropy(y) - (
                        p_l*self.entropy(y_l) + p_r*self.entropy(y_r)
                    )
                    split_info = -(p_l*np.log2(p_l) + p_r*np.log2(p_r))
                    score = gain / split_info if split_info != 0 else 0

                # CART
                else:
                    score = -(p_l*self.gini(y_l) + p_r*self.gini(y_r))

                if score > best_score:
                    best_score = score
                    best = (f, t)

        return best

    def build(self, X, y, depth):
        if len(set(y)) == 1 or depth == 0:
            return np.bincount(y).argmax()

        split = self.best_split(X, y)
        if split is None:
            return np.bincount(y).argmax()

        f, t = split
        X_l, X_r, y_l, y_r = self.split(X, y, f, t)

        return {
            "f": f,
            "t": t,
            "left": self.build(X_l, y_l, depth-1),
            "right": self.build(X_r, y_r, depth-1)
        }

    def fit(self, X, y):
        self.tree = self.build(X, y, self.depth)

    def predict_one(self, x, tree):
        if not isinstance(tree, dict):
            return tree

        if x[tree["f"]] < tree["t"]:
            return self.predict_one(x, tree["left"])
        return self.predict_one(x, tree["right"])

    def predict(self, X):
        return np.array([self.predict_one(x, self.tree) for x in X])


# ---------- Datasets ----------
datasets = {
    "Iris": load_iris(),
    "Wine": load_wine(),
    "Breast Cancer": load_breast_cancer()
}

algorithms = {
    "ID3": "id3",
    "C4.5": "c45",
    "CART": "cart"
}

results = []

# ---------- Training ----------
for d_name, data in datasets.items():

    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    for a_name, algo in algorithms.items():

        model = DT(algo=algo)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        results.append([
            d_name,
            a_name,
            round(accuracy_score(y_test, y_pred), 3),
            round(precision_score(y_test, y_pred, average='weighted'), 3),
            round(recall_score(y_test, y_pred, average='weighted'), 3),
            round(f1_score(y_test, y_pred, average='weighted'), 3)
        ])

# ---------- Comparison Table ----------
df = pd.DataFrame(results, columns=[
    "Dataset", "Algorithm",
    "Accuracy", "Precision",
    "Recall", "F1-Score"
])

print(df)

# Hidden Markov Model (HMM)
import numpy as np

def forward_algorithm(pi, A, B, observations, state_labels=None, obs_labels=None, verbose=True):
    pi = np.array(pi, dtype=float)
    A  = np.array(A,  dtype=float)
    B  = np.array(B,  dtype=float)
    T  = len(observations)
    N  = len(pi)

    if state_labels is None:
        state_labels = [f"s{i}" for i in range(N)]
    if obs_labels is None:
        obs_labels = [f"o{k}" for k in range(B.shape[1])]

    alpha = np.zeros((T, N))

    if verbose:
        print("=" * 60)
        print("  Hidden Markov Model — Forward Algorithm")
        print("=" * 60)
        obs_seq_str = ", ".join(obs_labels[o] for o in observations)
        print(f"\nObservation sequence O = ({obs_seq_str})")
        print(f"T = {T},  N = {N} states\n")

    o1 = observations[0]
    alpha[0] = pi * B[:, o1]

    if verbose:
        print("── Step 1 Initialization ──────────────────────────────")
        print(f"   Observation at t=1 : {obs_labels[o1]}\n")
        for i in range(N):
            print(f"   α₁({state_labels[i]}) = π({state_labels[i]}) × B({state_labels[i]},{obs_labels[o1]})"
                  f"  =  {pi[i]:.4f} × {B[i, o1]:.4f}  =  {alpha[0, i]:.6f}")

    if verbose:
        print()
    for t in range(1, T):
        ot = observations[t]
        if verbose:
            print(f"── Step 2 Induction  t={t+1}  (obs={obs_labels[ot]}) ──────────────")
        for j in range(N):
            summation = sum(alpha[t-1, i] * A[i, j] for i in range(N))
            alpha[t, j] = summation * B[j, ot]
            if verbose:
                terms = " + ".join(
                    f"α{t}({state_labels[i]})·a({state_labels[i]}→{state_labels[j]})"
                    for i in range(N)
                )
                print(f"   α{t+1}({state_labels[j]}) = [{terms}] × B({state_labels[j]},{obs_labels[ot]})")
                term_vals = " + ".join(
                    f"{alpha[t-1,i]:.6f}×{A[i,j]:.4f}" for i in range(N)
                )
                print(f"             = [{term_vals}] × {B[j, ot]:.4f}")
                print(f"             = {summation:.8f} × {B[j, ot]:.4f}  =  {alpha[t, j]:.8f}")
        if verbose:
            print()

    prob = alpha[T-1].sum()

    if verbose:
        print("── Step 3 Termination ─────────────────────────────────")
        terms = " + ".join(f"α{T}({state_labels[i]})={alpha[T-1,i]:.8f}" for i in range(N))
        print(f"   P(O|λ) = {terms}")
        print(f"\n   ✔  P(O|λ) = {prob:.8e}  ≈  {prob:.6f}")
        print("=" * 60)

    return prob, alpha


if __name__ == "__main__":
    state_labels = ["S", "C", "R"]
    obs_labels = ["W", "Sh", "Cl"]
    pi = [0.5, 0.3, 0.2]
    A = [
        [0.6, 0.3, 0.1],
        [0.4, 0.4, 0.2],
        [0.3, 0.3, 0.4],
    ]
    B = [
        [0.6, 0.3, 0.1],
        [0.3, 0.4, 0.3],
        [0.1, 0.3, 0.6],
    ]
    observations = [1, 1, 0]   
    prob, alpha = forward_algorithm(
        pi, A, B, observations,
        state_labels=state_labels,
        obs_labels=obs_labels,
        verbose=True,
    )
