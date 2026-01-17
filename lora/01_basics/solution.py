import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model


def solve(
    model: nn.Module,
    X: torch.Tensor,
    y: torch.Tensor,
    save_path: str,
    epochs: int = 100,
    lr: float = 0.01,
) -> nn.Module:
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["linear"],
    )

    peft_model = get_peft_model(model, lora_config)

    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(peft_model.parameters(), lr=lr)

    for _ in range(epochs):
        optimizer.zero_grad()
        output = peft_model(X)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()

    peft_model.save_pretrained(save_path)

    return peft_model
