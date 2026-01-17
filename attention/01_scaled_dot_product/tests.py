import torch

from test_utils import run_all


def run_tests(solve):
    torch.manual_seed(42)

    t3_Q = torch.randn(4, 8)
    t3_K = t3_Q.clone()
    t3_V = torch.eye(4)

    t4_Q = torch.randn(3, 16)
    t4_K = torch.randn(3, 16)
    t4_V = torch.randn(3, 32)

    t6_Q = torch.randn(1, 8)
    t6_K = torch.randn(1, 8)
    t6_V = torch.randn(1, 4)

    t7_Q = torch.randn(5, 10)
    t7_K = torch.randn(5, 10)
    t7_V = torch.eye(5)

    t8_Q = torch.randn(100, 64)
    t8_K = torch.randn(100, 64)
    t8_V = torch.randn(100, 64)

    t9_Q = torch.randn(3, 4, dtype=torch.float64)
    t9_K = torch.randn(3, 4, dtype=torch.float64)
    t9_V = torch.randn(3, 5, dtype=torch.float64)

    tests = [
        {
            "name": "basic 2x2 case",
            "inputs": {
                "Q": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
                "K": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
                "V": torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
            },
            "check": lambda r: r.shape == (2, 2),
            "fail_msg": lambda r: f"expected shape (2, 2), got {r.shape}",
        },
        {
            "name": "attention weights V by similarity",
            "inputs": {
                "Q": torch.tensor([[1.0, 0.0]]),
                "K": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
                "V": torch.tensor([[10.0], [20.0]]),
            },
            "check": lambda r: r[0, 0] < 15.0,
            "fail_msg": lambda r: f"expected output closer to 10, got {r[0, 0]:.2f}",
        },
        {
            "name": "Q=K gives strongest self-attention",
            "inputs": {"Q": t3_Q, "K": t3_K, "V": t3_V},
            "check": lambda r: torch.allclose(
                torch.diag(r), r.max(dim=1).values, atol=1e-5
            ),
            "fail_msg": "self-attention not highest on diagonal",
        },
        {
            "name": "handles different d_k and d_v",
            "inputs": {"Q": t4_Q, "K": t4_K, "V": t4_V},
            "check": lambda r: r.shape == (3, 32),
            "fail_msg": lambda r: f"expected shape (3, 32), got {r.shape}",
        },
        {
            "name": "scaling prevents softmax saturation",
            "inputs": {
                "Q": torch.ones(2, 64),
                "K": torch.ones(2, 64),
                "V": torch.tensor([[1.0], [2.0]]),
            },
            "check": lambda r: torch.allclose(r, torch.full_like(r, 1.5), atol=0.1),
            "fail_msg": lambda r: f"expected ~1.5 (uniform attention), got {r.flatten().tolist()}",
        },
        {
            "name": "single token returns V unchanged",
            "inputs": {"Q": t6_Q, "K": t6_K, "V": t6_V},
            "check": lambda r: torch.allclose(r, t6_V),
            "fail_msg": "single token should return V unchanged",
        },
        {
            "name": "attention weights sum to 1",
            "inputs": {"Q": t7_Q, "K": t7_K, "V": t7_V},
            "check": lambda r: torch.allclose(r.sum(dim=1), torch.ones(5), atol=1e-5),
            "fail_msg": lambda r: f"row sums should be 1, got {r.sum(dim=1).tolist()}",
        },
        {
            "name": "handles larger sequences without NaN",
            "inputs": {"Q": t8_Q, "K": t8_K, "V": t8_V},
            "check": lambda r: r.shape == (100, 64) and not torch.isnan(r).any(),
            "fail_msg": "expected shape (100, 64) with no NaN",
        },
        {
            "name": "preserves dtype",
            "inputs": {"Q": t9_Q, "K": t9_K, "V": t9_V},
            "check": lambda r: r.dtype == torch.float64,
            "fail_msg": lambda r: f"expected float64, got {r.dtype}",
        },
        {
            "name": "extreme similarity focuses attention",
            "inputs": {
                "Q": torch.tensor([[100.0, 0.0], [0.0, 100.0]]),
                "K": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
                "V": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
            },
            "check": lambda r: torch.allclose(
                r, torch.tensor([[1.0, 0.0], [0.0, 1.0]]), atol=0.01
            ),
            "fail_msg": "extreme similarity should focus attention to matching row",
        },
    ]

    run_all("scaled_dot_product", tests, solve)
