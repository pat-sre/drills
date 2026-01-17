import sys
from io import StringIO


class TestFailed(Exception):
    pass


def run_test(name, func, inputs, check, fail_msg):
    """
    Run a single test case.

    Args:
        name: Test description
        func: Function to test
        inputs: Dict of kwargs to pass to func
        check: Callable(result) -> bool
        fail_msg: Message to show on failure (str or callable(result) -> str)

    Returns True if passed, raises TestFailed if not.
    """
    old_stdout = sys.stdout
    sys.stdout = captured = StringIO()

    try:
        result = func(**inputs)
    except Exception as e:
        sys.stdout = old_stdout
        output = captured.getvalue()
        _print_failure(name, output, f"raised {type(e).__name__}: {e}")
        raise TestFailed()

    sys.stdout = old_stdout
    output = captured.getvalue()

    if result is None:
        _print_failure(
            name, output, "Function returned None - did you forget a return statement?"
        )
        raise TestFailed()

    if check(result):
        print(f"{name} ✓")
        return True
    else:
        msg = fail_msg(result) if callable(fail_msg) else fail_msg
        _print_failure(name, output, msg)
        raise TestFailed()


def _print_failure(name, output, msg):
    print(name)
    if output.strip():
        print("  --- your output ---")
        for line in output.rstrip().split("\n"):
            print(f"  {line}")
        print("  --- end output ---")
    print(f"  ✗ FAILED: {msg}")


def run_all(name, tests, func):
    """Run all tests, stop on first failure."""
    print(f"Running {name}...\n")
    for i, test in enumerate(tests, 1):
        try:
            run_test(
                f"Test {i}: {test['name']}",
                func,
                test["inputs"],
                test["check"],
                test["fail_msg"],
            )
        except TestFailed:
            print(f"\n{i - 1}/{len(tests)} tests passed")
            return
    print(f"\nAll {len(tests)} tests passed!")
