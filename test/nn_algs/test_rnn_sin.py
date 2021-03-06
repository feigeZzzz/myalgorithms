from algs.nn_algoritms.common.model import Model
from algs.nn_algoritms.common.layer import Dense, SimpleRNN

import numpy as np

data = np.linspace(-50, 50, 2000)
data = np.sin(data)

x = []
y = []
for i in range(1000):
    x.append(data[i:i + 50])
    y.append(data[i + 1:i + 51])

x = np.array(x).reshape(1000, 50, 1)
y = np.array(y).reshape(1000, 50, 1)

model = Model(lr=0.02, epoch=1000, loss="mse2d", optimizer='sgd', decay=0.9999)
model.add(SimpleRNN(hidden_activation='tanh',
                    output_activation='linear',
                    max_length=50,
                    features=1,
                    hiddenDimension=15,
                    outputsDimension=1))
model.fit(x, y, watch_loss=True)
y_pre = model.predict(x)
y_pre = y_pre[:, -1, :]

import matplotlib.pyplot as plt

plt.plot(y_pre)
plt.plot(data[50:1050])
