import torch
import torch.nn.functional as F

from test_utils import run_all


def run_tests(solve):
    torch.manual_seed(42)

    t1_Q, t1_K, t1_V = torch.randn(4, 8), torch.randn(4, 8), torch.randn(4, 16)
    t2_Q, t2_K, t2_V = torch.randn(5, 8), torch.randn(5, 8), torch.randn(5, 4)
    t3_Q, t3_K, t3_V = torch.randn(1, 8), torch.randn(1, 8), torch.randn(1, 4)
    t5_Q, t5_K, t5_V = torch.randn(4, 8), torch.randn(4, 8), torch.eye(4)
    t6_Q, t6_K, t6_V = torch.randn(5, 10), torch.randn(5, 10), torch.eye(5)
    t8_Q, t8_K, t8_V = torch.randn(3, 32), torch.randn(3, 32), torch.randn(3, 64)
    t9_Q, t9_K, t9_V = torch.randn(100, 64), torch.randn(100, 64), torch.randn(100, 64)
    t10_Q, t10_K, t10_V = torch.randn(4, 8), torch.randn(4, 8), torch.randn(4, 4)

    d_k = t10_Q.shape[-1]
    scores = t10_Q @ t10_K.T / (d_k**0.5)
    non_causal_result = F.softmax(scores, dim=-1) @ t10_V

    tests = [
        {
            "name": "correct output shape",
            "inputs": {"Q": t1_Q, "K": t1_K, "V": t1_V},
            "check": lambda r: r.shape == (4, 16),
            "fail_msg": lambda r: f"expected shape (4, 16), got {r.shape}",
        },
        {
            "name": "first token only attends to itself",
            "inputs": {"Q": t2_Q, "K": t2_K, "V": t2_V},
            "check": lambda r: torch.allclose(r[0], t2_V[0], atol=1e-5),
            "fail_msg": "first row should equal V[0]",
        },
        {
            "name": "single token returns V unchanged",
            "inputs": {"Q": t3_Q, "K": t3_K, "V": t3_V},
            "check": lambda r: torch.allclose(r, t3_V, atol=1e-5),
            "fail_msg": "single token should return V",
        },
        {
            "name": "causal masking prevents future attention",
            "inputs": {
                "Q": torch.tensor([[1.0, 0.0], [1.0, 0.0]]),
                "K": torch.tensor([[1.0, 0.0], [1.0, 0.0]]),
                "V": torch.tensor([[1.0], [2.0]]),
            },
            "check": lambda r: (
                torch.allclose(r[0], torch.tensor([1.0]), atol=1e-5)
                and torch.allclose(r[1], torch.tensor([1.5]), atol=1e-5)
            ),
            "fail_msg": lambda r: f"expected [1.0] and [1.5], got {r[0].item():.2f} and {r[1].item():.2f}",
        },
        {
            "name": "no attention to future positions",
            "inputs": {"Q": t5_Q, "K": t5_K, "V": t5_V},
            "check": lambda r: all(
                r[i, j] == 0.0 for i in range(4) for j in range(i + 1, 4)
            ),
            "fail_msg": "upper triangle should be zero",
        },
        {
            "name": "attention weights sum to 1",
            "inputs": {"Q": t6_Q, "K": t6_K, "V": t6_V},
            "check": lambda r: torch.allclose(r.sum(dim=1), torch.ones(5), atol=1e-5),
            "fail_msg": lambda r: f"row sums should be 1, got {r.sum(dim=1).tolist()}",
        },
        {
            "name": "last token attends to all positions",
            "inputs": {
                "Q": torch.ones(6, 4),
                "K": torch.ones(6, 4),
                "V": torch.arange(6, dtype=torch.float).unsqueeze(1),
            },
            "check": lambda r: torch.allclose(r[-1], torch.tensor([2.5]), atol=0.1),
            "fail_msg": lambda r: f"last token should average to 2.5, got {r[-1].item():.2f}",
        },
        {
            "name": "handles different d_k and d_v",
            "inputs": {"Q": t8_Q, "K": t8_K, "V": t8_V},
            "check": lambda r: r.shape == (3, 64),
            "fail_msg": lambda r: f"expected shape (3, 64), got {r.shape}",
        },
        {
            "name": "handles larger sequences without NaN",
            "inputs": {"Q": t9_Q, "K": t9_K, "V": t9_V},
            "check": lambda r: r.shape == (100, 64) and not torch.isnan(r).any(),
            "fail_msg": "expected shape (100, 64) with no NaN",
        },
        {
            "name": "causal differs from non-causal",
            "inputs": {"Q": t10_Q, "K": t10_K, "V": t10_V},
            "check": lambda r: not torch.allclose(
                r[1:], non_causal_result[1:], atol=1e-3
            ),
            "fail_msg": "causal and non-causal should differ for positions > 0",
        },
    ]

    run_all("causal_attention", tests, solve)
