import torch
import torch.nn.functional as F


def solve(
    X: torch.Tensor,
    W_q: torch.Tensor,
    W_k: torch.Tensor,
    W_v: torch.Tensor,
) -> torch.Tensor:
    """
    Compute self-attention with learned projections.

    Self-attention projects the input X into queries, keys, and values,
    then computes scaled dot-product attention.

    Steps:
        1. Project X to queries: Q = X @ W_q
        2. Project X to keys: K = X @ W_k
        3. Project X to values: V = X @ W_v
        4. Compute attention: softmax(Q @ K^T / sqrt(d_k)) @ V

    Args:
        X: Input tensor of shape (seq_len, d_model)
        W_q: Query projection matrix of shape (d_model, d_k)
        W_k: Key projection matrix of shape (d_model, d_k)
        W_v: Value projection matrix of shape (d_model, d_v)

    Returns:
        Attention output of shape (seq_len, d_v)
    """
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v

    d_k = Q.shape[-1]
    scores = Q @ K.T / (d_k**0.5)
    weights = F.softmax(scores, dim=-1)
    return weights @ V
