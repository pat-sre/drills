import torch
import torch.nn.functional as F

from test_utils import run_all


def run_tests(solve):
    torch.manual_seed(42)

    # Test 1 tensors
    t1_X = torch.randn(4, 8)
    t1_W_q, t1_W_k, t1_W_v, t1_W_o = (
        torch.randn(8, 8),
        torch.randn(8, 8),
        torch.randn(8, 8),
        torch.randn(8, 8),
    )

    # Test 2 tensors (single head = self-attention)
    t2_X = torch.randn(3, 4)
    t2_W_q, t2_W_k, t2_W_v = torch.randn(4, 4), torch.randn(4, 4), torch.randn(4, 4)
    t2_W_o = torch.eye(4)
    Q, K, V = t2_X @ t2_W_q, t2_X @ t2_W_k, t2_X @ t2_W_v
    t2_expected = F.softmax(Q @ K.T / (4**0.5), dim=-1) @ V

    # Test 3 tensors (various head counts)
    t3_X = torch.randn(4, 12)
    t3_W_q, t3_W_k, t3_W_v, t3_W_o = (
        torch.randn(12, 12),
        torch.randn(12, 12),
        torch.randn(12, 12),
        torch.randn(12, 12),
    )

    # Test 4 tensors (single token)
    t4_X = torch.randn(1, 8)
    t4_W_q, t4_W_k, t4_W_v, t4_W_o = (
        torch.randn(8, 8),
        torch.randn(8, 8),
        torch.randn(8, 8),
        torch.randn(8, 8),
    )
    t4_expected = (t4_X @ t4_W_v) @ t4_W_o

    # Test 5 tensors (different head counts)
    t5_X = torch.randn(4, 8)
    t5_W_q, t5_W_k, t5_W_v, t5_W_o = (
        torch.randn(8, 8),
        torch.randn(8, 8),
        torch.randn(8, 8),
        torch.randn(8, 8),
    )

    # Test 6 tensors (larger dimensions)
    t6_X = torch.randn(32, 64)
    t6_W_q, t6_W_k, t6_W_v, t6_W_o = (
        torch.randn(64, 64),
        torch.randn(64, 64),
        torch.randn(64, 64),
        torch.randn(64, 64),
    )

    # Test 7 tensors (output projection)
    t7_X = torch.randn(3, 4)
    t7_W_q, t7_W_k, t7_W_v = torch.randn(4, 4), torch.randn(4, 4), torch.randn(4, 4)
    t7_base = None  # Will be computed in check

    # Test 8 tensors (dtype)
    t8_X = torch.randn(3, 4, dtype=torch.float64)
    t8_W_q = torch.randn(4, 4, dtype=torch.float64)
    t8_W_k = torch.randn(4, 4, dtype=torch.float64)
    t8_W_v = torch.randn(4, 4, dtype=torch.float64)
    t8_W_o = torch.randn(4, 4, dtype=torch.float64)

    # Test 9 tensors (heads independent)
    t9_X = torch.randn(4, 4)
    t9_W_q, t9_W_k = torch.randn(4, 4), torch.randn(4, 4)
    t9_W_v = torch.randn(4, 4)
    t9_W_v_zeroed = t9_W_v.clone()
    t9_W_v_zeroed[:, 2:] = 0  # Zero second head
    t9_W_o = torch.eye(4)

    # Test 10 tensors (stress test)
    t10_X = torch.randn(128, 256)
    t10_W_q, t10_W_k, t10_W_v, t10_W_o = (
        torch.randn(256, 256),
        torch.randn(256, 256),
        torch.randn(256, 256),
        torch.randn(256, 256),
    )

    # Pre-compute values for tests that need them
    t5_r2 = solve(t5_X, t5_W_q, t5_W_k, t5_W_v, t5_W_o, num_heads=2)
    t7_base = solve(t7_X, t7_W_q, t7_W_k, t7_W_v, torch.eye(4), num_heads=2)

    # Check all head counts for test 3
    t3_all_pass = True
    for num_heads in [1, 2, 3, 4, 6, 12]:
        r = solve(t3_X, t3_W_q, t3_W_k, t3_W_v, t3_W_o, num_heads)
        if r.shape != (4, 12):
            t3_all_pass = False
            break

    tests = [
        {
            "name": "correct output shape",
            "inputs": {
                "X": t1_X,
                "W_q": t1_W_q,
                "W_k": t1_W_k,
                "W_v": t1_W_v,
                "W_o": t1_W_o,
                "num_heads": 2,
            },
            "check": lambda r: r.shape == (4, 8),
            "fail_msg": lambda r: f"expected shape (4, 8), got {r.shape}",
        },
        {
            "name": "single head equals self-attention",
            "inputs": {
                "X": t2_X,
                "W_q": t2_W_q,
                "W_k": t2_W_k,
                "W_v": t2_W_v,
                "W_o": t2_W_o,
                "num_heads": 1,
            },
            "check": lambda r: torch.allclose(r, t2_expected, atol=1e-5),
            "fail_msg": "single head with identity W_o should equal self-attention",
        },
        {
            "name": "works with various head counts",
            "inputs": {
                "X": t3_X,
                "W_q": t3_W_q,
                "W_k": t3_W_k,
                "W_v": t3_W_v,
                "W_o": t3_W_o,
                "num_heads": 1,
            },
            "check": lambda r: t3_all_pass,
            "fail_msg": "should work with head counts 1, 2, 3, 4, 6, 12",
        },
        {
            "name": "single token handled correctly",
            "inputs": {
                "X": t4_X,
                "W_q": t4_W_q,
                "W_k": t4_W_k,
                "W_v": t4_W_v,
                "W_o": t4_W_o,
                "num_heads": 2,
            },
            "check": lambda r: torch.allclose(r, t4_expected, atol=1e-5),
            "fail_msg": "single token should give (X @ W_v) @ W_o",
        },
        {
            "name": "different head counts produce different outputs",
            "inputs": {
                "X": t5_X,
                "W_q": t5_W_q,
                "W_k": t5_W_k,
                "W_v": t5_W_v,
                "W_o": t5_W_o,
                "num_heads": 4,
            },
            "check": lambda r: not torch.allclose(r, t5_r2, atol=1e-3),
            "fail_msg": "2 heads and 4 heads should give different results",
        },
        {
            "name": "handles larger dimensions without NaN",
            "inputs": {
                "X": t6_X,
                "W_q": t6_W_q,
                "W_k": t6_W_k,
                "W_v": t6_W_v,
                "W_o": t6_W_o,
                "num_heads": 8,
            },
            "check": lambda r: r.shape == (32, 64) and not torch.isnan(r).any(),
            "fail_msg": "expected shape (32, 64) with no NaN",
        },
        {
            "name": "output projection is applied",
            "inputs": {
                "X": t7_X,
                "W_q": t7_W_q,
                "W_k": t7_W_k,
                "W_v": t7_W_v,
                "W_o": torch.eye(4) * 2.0,
                "num_heads": 2,
            },
            "check": lambda r: torch.allclose(r, t7_base * 2.0, atol=1e-5),
            "fail_msg": "scaling W_o by 2 should scale output by 2",
        },
        {
            "name": "preserves dtype",
            "inputs": {
                "X": t8_X,
                "W_q": t8_W_q,
                "W_k": t8_W_k,
                "W_v": t8_W_v,
                "W_o": t8_W_o,
                "num_heads": 2,
            },
            "check": lambda r: r.dtype == torch.float64,
            "fail_msg": lambda r: f"expected float64, got {r.dtype}",
        },
        {
            "name": "heads operate independently",
            "inputs": {
                "X": t9_X,
                "W_q": t9_W_q,
                "W_k": t9_W_k,
                "W_v": t9_W_v_zeroed,
                "W_o": t9_W_o,
                "num_heads": 2,
            },
            "check": lambda r: torch.allclose(r[:, 2:], torch.zeros(4, 2), atol=1e-5),
            "fail_msg": "zeroing head 2's V should zero its output",
        },
        {
            "name": "stress test with long sequence",
            "inputs": {
                "X": t10_X,
                "W_q": t10_W_q,
                "W_k": t10_W_k,
                "W_v": t10_W_v,
                "W_o": t10_W_o,
                "num_heads": 8,
            },
            "check": lambda r: r.shape == (128, 256)
            and not torch.isnan(r).any()
            and not torch.isinf(r).any(),
            "fail_msg": "expected shape (128, 256) with no NaN/Inf",
        },
    ]

    run_all("multi_head_attention", tests, solve)
