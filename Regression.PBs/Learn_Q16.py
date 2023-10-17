#!/usr/bin/python3
#
# script to learn multi-output regression neural network to predict protein local structure
# by 16 protein blocks (de Brevern et al).
#
# (C) Yuri V. Milchevskiy, Yuri V. Kravatsky
# email: milch@eimb.ru
#
# Dependencies:
#  1. python 3 (tested with python 3.8.10)
#  2. numpy (tested with 1.22.3)
#  3. PyTorch (tested with 1.12.1)
#
######################################################################################

from torch.nn import Linear
from torch.nn import Module
from torch.nn.init import kaiming_uniform_
import torch.nn as nn
import torch
import numpy
import statistics
import sys
import os

#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

# If videocard has < 24G DRAM, disable test dataset for learning by test_enabled=0
test_enabled = 1

def printf(format, *args):
    sys.stdout.write(format % args)

def accuracy(yt, y_pred):
  # assumes model.eval()
  # granular but slow approach
  n_correct = 0; n_wrong = 0
  for i in range(len(yt)):
   t_index=torch.argmax(yt[i])
   pred_index=torch.argmax(y_pred[i])

   if t_index == pred_index:
    n_correct += 1
   else:
      n_wrong += 1

  acc = (n_correct * 1.0) / (n_correct + n_wrong)
  return acc

# model definition
class MultiOutputRegression(torch.nn.Module):
    # define model elements
    def __init__(self):
        super(MultiOutputRegression, self).__init__()
        # input to first hidden layer
        self.hidden1 = Linear(380, 320)
        kaiming_uniform_(self.hidden1.weight, nonlinearity='sigmoid')
        self.act1 = torch.nn.Sigmoid()

        # 2 hidden layer
        self.hidden2 = Linear(320, 180)
        kaiming_uniform_(self.hidden2.weight, nonlinearity='sigmoid')
        self.act2 = torch.nn.Sigmoid()

        # 3 hidden layer
        self.hidden3 = Linear(180, 90)
        kaiming_uniform_(self.hidden3.weight, nonlinearity='sigmoid')
        self.act3 = torch.nn.Sigmoid()

        # 4 hidden layer
        self.hidden4 = Linear(90, 50)
        kaiming_uniform_(self.hidden4.weight, nonlinearity='sigmoid')
        self.act4 = torch.nn.Sigmoid()

        # 5 hidden layer and output
        self.hidden5 = Linear(50, 16)

    # forward propagate input
    def forward(self, X):
        # input to first hidden layer
        X = self.hidden1(X)
        X = self.act1(X)
        # 2 hidden layer
        X = self.hidden2(X)
        X = self.act2(X)
        # 3 hidden layer
        X = self.hidden3(X)
        X = self.act3(X)
        # 4 hidden layer
        X = self.hidden4(X)
        X = self.act4(X)

        # output layer
        X = self.hidden5(X)
        return X

model = MultiOutputRegression()

if torch.cuda.is_available():
    dev = "cuda:0"
else: 
    dev = "cpu"
device = torch.device(dev)

# If you want to begin from the scratch, delete these files:
BestModelName 		= 'Q16_DATA_MODEL'
BestModelName_CPU 	= 'Q16_DATA_MODEL_FOR_CPU'

if( os.path.exists(BestModelName)):
	model=torch.load(BestModelName)
	model.eval()

model = model.to(device)

criterion = nn.MSELoss()
print(criterion)

# if you want to begin from the scratch, you should set lr_start to 0.01
lr_start = 0.0001
optimizer = torch.optim.Adam(model.parameters(),lr=lr_start)

X = numpy.load("train_Q16X.npy")
y = numpy.load("train_Q16Y.npy")

X = X.astype('float16')
y = y.astype('float16')

Xt=torch.from_numpy(X).float().to(device)
yt=torch.from_numpy(y).float().to(device)
del X
del y

print(Xt)
print(yt)

print(Xt.shape)
print(yt.shape)

if test_enabled == 1:
    X = numpy.load("test_Q16X.npy")
    y = numpy.load("test_Q16Y.npy")

    X = X.astype('float16')
    y = y.astype('float16')

    Xtest=torch.from_numpy(X).float().to(device)
    ytest=torch.from_numpy(y).float().to(device)
    del X
    del y

X = numpy.load("CB513X.npy")
y = numpy.load("CB513Y.npy")

X = X.astype('float16')
y = y.astype('float16')

Xtest_1=torch.from_numpy(X).float().to(device)
ytest_1=torch.from_numpy(y).float().to(device)

del X
del y

print(Xtest_1.shape)
print(ytest_1.shape)

kk=0
prevloss=1000000
losses = []
learned = 0

for epoch in range(500):
    if learned==1:
        break
    for i in range(1, 500):
        optimizer.zero_grad()
        y_pred = model(Xt)
        loss = criterion(y_pred, yt)
        losses.append(loss.item())

        loss.backward()
        optimizer.step()
        kk=kk+1
        if kk%1000==1:
            lossmedian = statistics.median(losses)
            printf("kk = %d, loss = %.6f, step = %.7f\n", kk-1, lossmedian, lr_start)

            if kk > 5000 and lossmedian > prevloss:
                lr_start /= 5.0
                optimizer = torch.optim.AdamW(model.parameters(), lr=lr_start)

            prevloss = lossmedian
            losses.clear()

            y_pred_test_1 = model(Xtest_1)
            q16=accuracy(ytest_1, y_pred_test_1)
            print('Q16 for CB513 ', q16)

            q16l=accuracy(yt, y_pred)
            print('Q16 for learning sample ', q16l)

            torch.save(model,BestModelName)
            torch.save(model.state_dict(), BestModelName_CPU)

            if (q16 > 0.8101):
                printf ('Accuracy above 81%% is achieved, final step = %.7f !', lr_start)
                learned = 1
                break

y_pred = model(Xt)
q16=accuracy(yt, y_pred)
printf("Final Q16 for learning sample %lf\n",q16)
y_pred_test_1 = model(Xtest_1)
q16=accuracy(ytest_1, y_pred_test_1)
printf("Final Q16 for CB513 %lf\n", q16)

if test_enabled == 1:
    y_pred_test = model(Xtest)
    q16t=accuracy(ytest, y_pred_test)
    printf("Final Q16 for test sample %lf\n",q16t)

y_pred=y_pred.cpu().detach().numpy() 
yt=yt.cpu().detach().numpy()

torch.save(model,BestModelName)
torch.save(model.state_dict(), BestModelName_CPU)

numpy.savetxt("y_pred.csv", y_pred , delimiter="\t")
numpy.savetxt("yt.csv", yt, delimiter="\t")
