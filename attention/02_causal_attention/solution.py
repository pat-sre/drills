import torch
import torch.nn.functional as F


def solve(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor) -> torch.Tensor:
    """
    Compute scaled dot-product attention with causal mask.

    Causal masking prevents each position from attending to future positions.
    This is essential for autoregressive models (e.g., GPT) where predictions
    at position i should only depend on positions 0..i.

    The mask is lower-triangular: position i can attend to positions 0..i.
    Masked positions are set to -inf before softmax, resulting in 0 attention weight.

    Args:
        Q: Query tensor of shape (seq_len, d_k)
        K: Key tensor of shape (seq_len, d_k)
        V: Value tensor of shape (seq_len, d_v)

    Returns:
        Attention output of shape (seq_len, d_v)
    """
    seq_len = Q.shape[0]
    d_k = Q.shape[-1]

    scores = Q @ K.T
    scores = scores / (d_k**0.5)

    mask = torch.tril(torch.ones(seq_len, seq_len, dtype=torch.bool, device=Q.device))
    scores = scores.masked_fill(~mask, float("-inf"))

    weights = F.softmax(scores, dim=-1)
    return weights @ V
