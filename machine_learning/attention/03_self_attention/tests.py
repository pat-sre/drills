import torch
import torch.nn.functional as F

from test_utils import run_all


def run_tests(solve):
    torch.manual_seed(42)

    t1_X = torch.randn(4, 8)
    t1_W_q, t1_W_k, t1_W_v = torch.randn(8, 6), torch.randn(8, 6), torch.randn(8, 10)

    t2_X = torch.randn(3, 4)
    t2_W_q, t2_W_k, t2_W_v = torch.eye(4), torch.eye(4), torch.eye(4)
    t2_scores = t2_X @ t2_X.T / (4**0.5)
    t2_expected = F.softmax(t2_scores, dim=-1) @ t2_X

    t3_X = torch.randn(1, 8)
    t3_W_q, t3_W_k, t3_W_v = torch.randn(8, 4), torch.randn(8, 4), torch.randn(8, 6)
    t3_expected = t3_X @ t3_W_v

    t4_X = torch.randn(5, 16)
    t4_W_q, t4_W_k, t4_W_v = torch.randn(16, 8), torch.randn(16, 8), torch.randn(16, 32)

    t6_X = torch.zeros(4, 8)
    t6_W_q, t6_W_k, t6_W_v = torch.randn(8, 4), torch.randn(8, 4), torch.randn(8, 6)

    t7_X = torch.randn(3, 4)
    t7_W_q, t7_W_k, t7_W_v = torch.randn(4, 2), torch.randn(4, 2), torch.randn(4, 5)

    t8_X = torch.randn(100, 64)
    t8_W_q, t8_W_k, t8_W_v = (
        torch.randn(64, 32),
        torch.randn(64, 32),
        torch.randn(64, 64),
    )

    t9_X = torch.randn(3, 4, dtype=torch.float64)
    t9_W_q = torch.randn(4, 2, dtype=torch.float64)
    t9_W_k = torch.randn(4, 2, dtype=torch.float64)
    t9_W_v = torch.randn(4, 3, dtype=torch.float64)

    torch.manual_seed(123)
    t10_X = torch.randn(4, 6)
    t10_W_q, t10_W_k, t10_W_v = torch.randn(6, 3), torch.randn(6, 3), torch.randn(6, 5)
    Q, K, V = t10_X @ t10_W_q, t10_X @ t10_W_k, t10_X @ t10_W_v
    t10_expected = F.softmax(Q @ K.T / (3**0.5), dim=-1) @ V

    tests = [
        {
            "name": "correct output shape",
            "inputs": {"X": t1_X, "W_q": t1_W_q, "W_k": t1_W_k, "W_v": t1_W_v},
            "check": lambda r: r.shape == (4, 10),
            "fail_msg": lambda r: f"expected shape (4, 10), got {r.shape}",
        },
        {
            "name": "identity projections give raw self-attention",
            "inputs": {"X": t2_X, "W_q": t2_W_q, "W_k": t2_W_k, "W_v": t2_W_v},
            "check": lambda r: torch.allclose(r, t2_expected, atol=1e-5),
            "fail_msg": "identity projections should give raw self-attention on X",
        },
        {
            "name": "single token returns V projection",
            "inputs": {"X": t3_X, "W_q": t3_W_q, "W_k": t3_W_k, "W_v": t3_W_v},
            "check": lambda r: torch.allclose(r, t3_expected, atol=1e-5),
            "fail_msg": "single token should return X @ W_v",
        },
        {
            "name": "handles different d_k and d_v",
            "inputs": {"X": t4_X, "W_q": t4_W_q, "W_k": t4_W_k, "W_v": t4_W_v},
            "check": lambda r: r.shape == (5, 32),
            "fail_msg": lambda r: f"expected shape (5, 32), got {r.shape}",
        },
        {
            "name": "zero input gives zero output",
            "inputs": {"X": t6_X, "W_q": t6_W_q, "W_k": t6_W_k, "W_v": t6_W_v},
            "check": lambda r: torch.allclose(r, torch.zeros(4, 6), atol=1e-5),
            "fail_msg": "zero input should produce zero output",
        },
        {
            "name": "projections transform the input",
            "inputs": {"X": t7_X, "W_q": t7_W_q, "W_k": t7_W_k, "W_v": t7_W_v},
            "check": lambda r: r.shape == (3, 5),
            "fail_msg": lambda r: f"expected shape (3, 5), got {r.shape}",
        },
        {
            "name": "handles larger sequences without NaN",
            "inputs": {"X": t8_X, "W_q": t8_W_q, "W_k": t8_W_k, "W_v": t8_W_v},
            "check": lambda r: r.shape == (100, 64) and not torch.isnan(r).any(),
            "fail_msg": "expected shape (100, 64) with no NaN",
        },
        {
            "name": "preserves dtype",
            "inputs": {"X": t9_X, "W_q": t9_W_q, "W_k": t9_W_k, "W_v": t9_W_v},
            "check": lambda r: r.dtype == torch.float64,
            "fail_msg": lambda r: f"expected float64, got {r.dtype}",
        },
        {
            "name": "matches manual computation",
            "inputs": {"X": t10_X, "W_q": t10_W_q, "W_k": t10_W_k, "W_v": t10_W_v},
            "check": lambda r: torch.allclose(r, t10_expected, atol=1e-5),
            "fail_msg": "output doesn't match manual computation",
        },
    ]

    run_all("self_attention", tests, solve)
