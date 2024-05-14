import numpy as np

def relu(z):
    return np.maximum(z, 0)

def sigmoid(z):
    g = np.zeros(z.size)
    g = 1/(1+np.exp(-z))
    return g

def cost_function(theta, X, y):
    m = y.size

    cost = 0
    grad = np.zeros(theta.shape)

    for i in range(m):
        cost += ((-y[i]) * np.log(sigmoid(np.dot(theta,X[i]))) - (1-y[i]) * np.log(1-sigmoid(np.dot(theta,X[i]))))/m
        grad += (sigmoid(np.dot(theta,X[i]))-y[i])*X[i]/m
    print(cost, grad)
    return cost, grad