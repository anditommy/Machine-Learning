import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

plt.style.use('seaborn')


def r2_score(y, y_pred):
    mean_y = np.mean(y)
    ss_tot = sum((y - mean_y)**2)
    ss_res = sum((y - y_pred)**2)
    r2 = 1 - (ss_res / ss_tot)

    return r2


def rmse(y, y_pred):
    return np.sqrt(sum((y - y_pred)**2) / len(y))


def create_linear_dataset(n_data, m=2, b=1, variance=True):

    xs = np.linspace(-1, 1, n_data)
    ys = m * xs + b

    if variance:
        ys += np.random.random_sample(n_data)

    return np.array(xs).reshape(-1, 1), np.array(ys).reshape(-1, 1)


X, y = create_linear_dataset(n_data=100, b=1, m=2)

ones = np.ones((len(X), 1))
x = np.concatenate((ones, X), axis=1)

theta = np.random.random((x.shape[-1], 1))
theta = np.array([3.5, 0])  # just for visualization, else comment it
alpha = 1e-2
max_epoch = 10
m = len(y)
indices = list(range(m))

history = {
    'theta': [],
    'cost': []
}

# ------------------------STOCHASTIC GRADIENT DESCENT----------------------

for epoch in range(max_epoch):
    random.shuffle(indices)

    # gradient descent per feature set
    for i in indices:
        _x = x[i]  # single sample
        _y = y[i]  # single sample

        hypothesis = np.dot(_x, theta)
        cost = (hypothesis - _y)**2 / 2
        gradients = ((hypothesis - _y) * _x)
        theta = theta - alpha * gradients

        history["theta"].append(theta.squeeze().tolist())
        history['cost'].append(cost)

y_pred = theta[0] + theta[1] * X

print('\nTheta:', theta.squeeze().tolist())
print('R2 Score:', r2_score(y, y_pred))
print('RMSE:', rmse(y, y_pred))

# -------------------------------VISUALIZATION--------------------------------

y_pred = []
for i in range(len(history['cost'])):
    b, m = history["theta"][i][0], history["theta"][i][1]
    prediction = m * X + b
    y_pred.append(prediction)

name = 'Stochastic'

fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.scatter(X, y, label='Original Data')
line1, = ax1.plot([], [], alpha=0.6, color='r', label='Hypothesis')
ax1.set_title(f'{name} Gradient Descent')
ax1.set_xlabel('X data')
ax1.set_ylabel('Y data')
ax1.legend(loc='upper left')

line2, = ax2.plot([], color='g', label='Cost')
ax2.set_title(f'{name} - Training History Cost')
ax2.set_xlabel('Iteration')
ax2.set_ylabel('Cost')
ax2.legend(loc='upper right')

x_cost, y_cost = [], []


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2


def animate(i):
    b, m = history["theta"][i][0], history["theta"][i][1]
    prediction = m * X + b

    x_cost.append(i)
    y_cost.append(history["cost"][i])

    xmin, xmax = ax2.get_xlim()
    if i >= xmax:
        ax2.set_xlim(xmin, 2 * xmax)
        ax2.figure.canvas.draw()
    elif i < xmin:
        ax2.set_xlim(xmin / 2, xmax)
        ax2.figure.canvas.draw()

    ymin, ymax = ax2.get_ylim()

    if history['cost'][i] >= ymax:
        ax2.set_ylim(ymin, history['cost'][i] + 0.5)
        ax2.figure.canvas.draw()
    elif history["cost"][i] < ymin:
        ax2.set_xlim(ymin / 2, ymax)
        ax2.figure.canvas.draw()

    line1.set_data(X, prediction)
    line2.set_data(x_cost, y_cost)

    return line1, line2


ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=len(y_pred), blit=True,
                              interval=1, repeat=False)

# saves the animation as .mp4 (takes time, comment if needed)
mywriter = animation.FFMpegWriter(fps=60)
ani.save(f'{name} Gradient Descent.mp4', writer=mywriter)
# show the animation
plt.show()
