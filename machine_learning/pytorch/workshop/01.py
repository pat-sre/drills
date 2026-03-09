import torch

x1 = torch.tensor([45.0])
y1 = torch.tensor([500.0])

x2 = torch.tensor([70.0])
y2 = torch.tensor([750.0])

w = torch.tensor([10.0], requires_grad=True)
b = torch.tensor([5.0], requires_grad=True)

out1 = x1 * w + b
out2 = x2 * w + b
print(out1, out2)

rmse = torch.sqrt(((y1 - out1) ** 2 + (y2 - out2) ** 2) / 2)
print("RMSE1:", rmse)
rmse.backward()
print(w.grad, b.grad)

lr = 1e-2
with torch.no_grad():
    w -= lr * w.grad
    b -= lr * b.grad

out1 = x1 * w + b
out2 = x2 * w + b
print(out1, out2)
w.grad.zero_()
b.grad.zero_()
rmse = torch.sqrt(((y1 - out1) ** 2 + (y2 - out2) ** 2) / 2)
print("RMSE2:", rmse)
rmse.backward()
print(w.grad, b.grad)
with torch.no_grad():
    w -= lr * w.grad
    b -= lr * b.grad

out1 = x1 * w + b
out2 = x2 * w + b
print(out1, out2)
w.grad.zero_()
b.grad.zero_()
rmse = torch.sqrt(((y1 - out1) ** 2 + (y2 - out2) ** 2) / 2)
print("RMSE3:", rmse)
rmse.backward()
print(w.grad, b.grad)
with torch.no_grad():
    w -= lr * w.grad
    b -= lr * b.grad

out1 = x1 * w + b
out2 = x2 * w + b
print(out1, out2)
