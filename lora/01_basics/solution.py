# Implement basic LoRA (Low-Rank Adaptation) training with PEFT.
#
# Steps:
#   1. Create a LoraConfig targeting the "linear" layer
#   2. Wrap the model with get_peft_model()
#   3. Train the model using a basic training loop
#   4. Save only the LoRA adapters (not the full model)
#
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model


def train_lora(
    model: nn.Module,
    X: torch.Tensor,
    y: torch.Tensor,
    save_path: str,
    epochs: int = 100,
    lr: float = 0.01,
) -> nn.Module:
    """
    Apply LoRA adapters to model, train, and save adapters.
    """
    # 1. Create LoRA config
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["linear"],
    )

    # 2. Wrap model with LoRA adapters
    peft_model = get_peft_model(model, lora_config)

    # 3. Train using basic training loop
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(peft_model.parameters(), lr=lr)

    for _ in range(epochs):
        optimizer.zero_grad()
        output = peft_model(X)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()

    # 4. Save only the LoRA adapters
    peft_model.save_pretrained(save_path)

    return peft_model


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train_lora)
