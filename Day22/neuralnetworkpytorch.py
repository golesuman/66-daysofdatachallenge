# -*- coding: utf-8 -*-
"""neuralnetworkPytorch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XmfuoLn_rD86951hsUgEPzvq27QfO0nT
"""

# importing dependencies and libraries
import torch.nn as nn
import torch.optim as optimizer
import torch.nn.functional as functional
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transform
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# hyper parameters
input_size=784
hidden_size=100
num_classes=10
num_epochs=3
batch_size=100
learning_rate=0.001
# importing data MNIST
training_data=datasets.MNIST(root='./data',train=True,transform=transform.ToTensor(),download=True)
test_data=datasets.MNIST(root='./data',train=False,transform=transform.ToTensor())
train_loader=DataLoader(dataset=training_data,batch_size=batch_size,shuffle=True)
test_loader=DataLoader(dataset=test_data,batch_size=batch_size)
examples=iter(train_loader)
samples,labels=examples.next()
print(samples.shape)
print(labels.shape)

class NeuralNet(nn.Module):
  def __init__(self,input_size,hidden_size,num_classes):
    super(NeuralNet,self).__init__()
    self.l1=nn.Linear(input_size,hidden_size)
    self.relu=nn.ReLU()
    self.l2=nn.Linear(hidden_size,num_classes)

  def forward(self,x):
    out=self.l1(x)
    out=self.relu(out)
    out=self.l2(out)
    return out

model=NeuralNet(input_size,hidden_size,num_classes).to(device)
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
criterio=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.parameters(),lr=learning_rate)
# training loop
n_total_steps=len(train_loader)
for epoch in range(num_epochs):
  for i, (images,labels) in enumerate(train_loader):
    # 100,1,28,28
    # 100,784 
    images=images.reshape(-1,28*28).to(device)
    labels=labels.to(device)
    # forward pass
    output=model(images)
    loss=criterio(output,labels)
    # backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (i+1)%100==0:
      print(f'epoch {epoch+1}/{num_epochs},step{i+1}/{n_total_steps},loss={loss.item():.4f}')
#test
with torch.no_grad():
  n_correct=0
  n_samples=0
  for images,labels in test_loader:
    images=images.reshape(-1,28*28).to(device)
    labels=labels.to(device)
    outputs=model(images)
    #value,index
    _, predictions=torch.max(output,1)
    n_samples+=labels.shape[0]
    n_correct+=(predictions==labels).sum().item()
  acc=n_correct/n_samples
  print(f'The accuracy is {acc}')

use_cuda=torch.cuda.get_device_name()
print(use_cuda)

torch.cuda.current_device()

train_loader.device()

