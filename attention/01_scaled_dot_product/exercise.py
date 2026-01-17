import torch


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
    softmax_numerator = torch.nn.Softmax(Q @ K.transpose)
    print(Q.shape, K.shape)
    softmax_denominator = 1
