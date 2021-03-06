import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import sys
from torch.utils.data import TensorDataset, DataLoader

#   Title: Neural Networks Tutorial
#   Author: Chintala, S
#   Date: 9/14/2017
#   Code version: 1.0
#   Source: http://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html

# Hyperparameters:
epochs = 1
batchSize = 100

class Net(nn.Module):

    def __init__(self, sizes):
        super(Net, self).__init__()
        # 2x2 square convolution
        self.conv1 = nn.Conv2d(1, 1, [2,1])
        self.conv2 = nn.Conv2d(1, 1, [2,1])
        self.conv3 = nn.Conv2d(1, 1, [2,1])
        self.conv4 = nn.Conv2d(1, 1, [2,1])
        self.conv5 = nn.Conv2d(1, 1, [2,1])
        # Convolutional to linear neuron
        self.fc1 = nn.Linear(sizes[0], sizes[1])
        self.fc2 = nn.Linear(sizes[1], sizes[2])
        self.fc3 = nn.Linear(sizes[2], sizes[3])
        self.fc4 = nn.Linear(sizes[3], sizes[4])
        self.fc5 = nn.Linear(sizes[4], 1)

    def forward(self, x):
        # Max pooling over a (1, 1) window
        #print(x.size())
        x = F.max_pool2d(F.relu(self.conv1(x)), [1,1])
        #print(x.size())
        x = F.max_pool2d(F.relu(self.conv2(x)), [1,1])
        #print(x.size())
        x = F.max_pool2d(F.relu(self.conv3(x)), [1,1])
        #print(x.size())
        x = F.max_pool2d(F.relu(self.conv4(x)), [1,1])
        #print(x.size())
        x = x.view(-1, self.num_flat_features(x))
        #print(x.size())
        x = self.fc1(x)
        #print(x.size())
        x = self.fc2(x)
        #print(x.size())
        x = self.fc3(x)
        #print(x.size())
        x = self.fc4(x)
        #print(x.size())
        x = self.fc5(x)
        #print(x.size())
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

#   Title: PyTorch with Examples
#   Author: Johnson, J
#   Date: 2017
#   Code version: 1.0
#   Availability: http://pytorch.org/tutorials/beginner/pytorch_with_examples.html#nn-module

model = Net([643, 160, 40, 10, 2])
xFiles = ['01_03','01_15','01_16','01_21','01_26','03_01','03_03','03_04','03_34','03_36','05_06','05_13','05_16','05_17','05_22']
xtestFiles = ['01_04','01_18','03_02','03_35']
x = []
y = []
for a in range(len(xFiles)):
    xsample = np.load('Xs\\chb'+xFiles[a]+'.npy')
    ysample = np.load('Ys\\chb'+xFiles[a]+'.npy')
    for a in range(len(xsample)):
        x.append(xsample[a])
        y.append(ysample[a])
xtest = []
ytest = []
for a in range(len(xtestFiles)):
    xsample = np.load('Xs\\chb'+xtestFiles[a]+'.npy')
    ysample = np.load('Ys\\chb'+xtestFiles[a]+'.npy')
    for a in range(len(xsample)): 
        xtest.append(xsample[a])
        ytest.append(ysample[a])
#blank data inputs
#x = []
#y = [26, 21, 16, 11, 6, 1, 7, 2, 135, 130, 125, 120, 115, 110, 105, 100, 95, 90, 85, 80]
#xtest = []
#ytest = [26, 21, 16, 11, 6]
#sample = []
#for a in range(643):
#    sample.append(0)
#for a in range(20):
#    x.append(sample)
#for a in range(5):
#    xtest.append(sample)

#creating eligible groups of five samples for input
#training data set
xtrain = []
ytrain = []
n = 0
for a in range(len(x)):
    n += 1
    if y[a] > 5:
        if n > 4:
            xtrain.append([x[a-4], x[a-3], x[a-2], x[a-1], x[a]])
            ytrain.append([y[a]])
            n = 0
    else:
        n = 0
#testing data set
xset = []
yset = []
n = 0
for a in range(len(xtest)):
    n += 1
    if ytest[a] > 5:
        if n > 4:
            xset.append([xtest[a-4], xtest[a-3], xtest[a-2], xtest[a-1], xtest[a]])
            yset.append([ytest[a]])
            n = 0
    else:
        n = 0
xtest = np.array(xset)
ytest = np.array(yset)
x = np.array(xtrain)
y = np.array(ytrain)
x = Variable(torch.from_numpy(x).float()).unsqueeze(1)
y = Variable(torch.from_numpy(y).float(), requires_grad=False)
xtest = Variable(torch.from_numpy(xtest).float(), requires_grad=False).unsqueeze(1)
ytest = Variable(torch.from_numpy(ytest).float(), requires_grad=False)

trainset = TensorDataset(x,y)
loader = DataLoader(trainset, batch_size=batchSize, shuffle=True)
testset = TensorDataset(xtest,ytest)
testloader = DataLoader(testset, batch_size=batchSize, shuffle=True)

criterion = torch.nn.MSELoss(reduction='sum')
optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
errorTime = []
testErrorTime = []

for t in range(epochs):
    for (x,y) in loader:
        y_pred = model(Variable(x))
        loss = criterion(y_pred, Variable(y))
        print(t, loss.data[0])
        errorTime.append(loss.data.item())
        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    for (xtest,ytest) in testloader:
        test_pred = model(xtest)
        testLoss = criterion(test_pred, ytest)
        testErrorTime.append(testLoss.data.item())

import matplotlib.pyplot as plt
xs = range(len(errorTime))
ys = errorTime
plt.plot(xs, ys)
xsb = range(len(testErrorTime))
ysb = testErrorTime
plt.plot(xsb, ysb)
plt.show()
