import torch
import torch.nn.functional as F


def solve(
    X: torch.Tensor,
    W_q: torch.Tensor,
    W_k: torch.Tensor,
    W_v: torch.Tensor,
    W_o: torch.Tensor,
    num_heads: int,
) -> torch.Tensor:
    """
    Compute multi-head attention.

    Multi-head attention runs multiple attention operations in parallel,
    each with its own learned projections (heads), then concatenates
    and projects the results.

    Steps:
        1. Project X to Q, K, V using W_q, W_k, W_v
        2. Split Q, K, V into num_heads separate heads
        3. Apply scaled dot-product attention to each head
        4. Concatenate all head outputs
        5. Project concatenated output using W_o

    The projection matrices W_q, W_k, W_v have shape (d_model, d_model),
    containing all heads' projections concatenated. Each head operates
    on d_k = d_model // num_heads dimensions.

    Args:
        X: Input tensor of shape (seq_len, d_model)
        W_q: Query projection of shape (d_model, d_model)
        W_k: Key projection of shape (d_model, d_model)
        W_v: Value projection of shape (d_model, d_model)
        W_o: Output projection of shape (d_model, d_model)
        num_heads: Number of attention heads

    Returns:
        Output tensor of shape (seq_len, d_model)
    """
    seq_len, d_model = X.shape
    d_head = d_model // num_heads

    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v

    Q = Q.view(seq_len, num_heads, d_head).transpose(0, 1)
    K = K.view(seq_len, num_heads, d_head).transpose(0, 1)
    V = V.view(seq_len, num_heads, d_head).transpose(0, 1)

    scores = Q @ K.transpose(-2, -1) / (d_head**0.5)
    weights = F.softmax(scores, dim=-1)
    head_outputs = weights @ V

    concat = head_outputs.transpose(0, 1).contiguous().view(seq_len, d_model)
    return concat @ W_o
