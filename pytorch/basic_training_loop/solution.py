import torch
import torch.nn as nn
import torch.optim as optim

dataset_size = 1000
X = torch.tensor([float(i) for i in range(dataset_size)])
y = torch.tensor([x / 2 for x in X])

model = nn.Linear(1, 1)
loss = nn.MSELoss()
optimizer = optim.SGD(model.parameters())

for epoch in range(10):
    epoch_loss = 0
    for i in range(dataset_size):
    # for each sample:
        # zero_grad  ← clear accumulated gradients
        model.zero_grad()
        # forward
        input_data = torch.tensor([X[i]])
        target_data = torch.tensor([y[i]])
        out = model(input_data)
        # loss
        loss_out = loss(out, target_data)
        epoch_loss += loss_out
        # backward
        loss_out.backward()
        # step  ← update weights
        optimizer.step()
    print(epoch_loss)
