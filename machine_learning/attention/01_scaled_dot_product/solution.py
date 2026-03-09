import torch
import torch.nn.functional as F


def solve(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor) -> torch.Tensor:
    """
    Compute scaled dot-product attention.

    Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

    Args:
        Q: Query tensor of shape (seq_len, d_k)
        K: Key tensor of shape (seq_len, d_k)
        V: Value tensor of shape (seq_len, d_v)

    Returns:
        Attention output of shape (seq_len, d_v)
    """
    d_k = Q.shape[-1]
    scores = Q @ K.T
    scores = scores / (d_k**0.5)
    weights = F.softmax(scores, dim=-1)
    return weights @ V
