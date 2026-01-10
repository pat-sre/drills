import subprocess
import sys
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .config import CODE_TIMEOUT, MAX_CODE_SIZE, PROJECT_ROOT
from .exercises import get_test_config


class ErrorType(str, Enum):
    """Type of execution error."""

    TIMEOUT = "timeout"
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    TEST_FAILURE = "test_failure"


# Marker for structured success detection
SUCCESS_MARKER = "___DRILLS_ALL_TESTS_PASSED___"


@dataclass
class RunResult:
    """Result of running user code."""

    passed: bool
    output: str
    error_type: ErrorType | None = None

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "output": self.output,
            "error_type": self.error_type.value if self.error_type else None,
        }


def _classify_error(stderr: str) -> ErrorType:
    """Classify error type from stderr output."""
    stderr_lower = stderr.lower()

    if "syntaxerror" in stderr_lower or "indentationerror" in stderr_lower:
        return ErrorType.SYNTAX
    if "assertionerror" in stderr_lower or "test failed" in stderr_lower:
        return ErrorType.TEST_FAILURE

    return ErrorType.RUNTIME


def run_code(topic: str, name: str, code: str) -> RunResult:
    """Execute user code and run tests."""
    # Validate code size
    code_size = len(code.encode("utf-8"))
    if code_size > MAX_CODE_SIZE:
        return RunResult(
            passed=False,
            output=f"Code too large: {code_size} bytes (max {MAX_CODE_SIZE})",
            error_type=ErrorType.RUNTIME,
        )

    config = get_test_config(topic, name)
    project_root_str = str(PROJECT_ROOT.resolve())

    runner_script = f'''import sys
sys.path.insert(0, r"{project_root_str}")

# Prevent user's if __name__ == "__main__" block from running
__name__ = "__exercise__"

# User's code
{code}

# Run tests with structured result reporting
try:
    {config["test_import"]}
    {config["test_call"]}
    print("{SUCCESS_MARKER}")
except AssertionError as e:
    print(f"Test failed: {{e}}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {{e}}", file=sys.stderr)
    sys.exit(1)
'''

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(runner_script)
        script_path = Path(f.name)

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=CODE_TIMEOUT,
            cwd=str(PROJECT_ROOT.resolve()),
        )

        output = result.stdout + result.stderr

        # Check for structured success marker
        if SUCCESS_MARKER in output:
            clean_output = output.replace(SUCCESS_MARKER, "").strip()
            return RunResult(passed=True, output=clean_output or "All tests passed!")

        # Determine error type
        error_type = _classify_error(result.stderr)
        return RunResult(passed=False, output=output, error_type=error_type)

    except subprocess.TimeoutExpired:
        return RunResult(
            passed=False,
            output=f"Timeout: code took longer than {CODE_TIMEOUT} seconds",
            error_type=ErrorType.TIMEOUT,
        )
    except OSError as e:
        return RunResult(
            passed=False,
            output=f"Execution error: {e}",
            error_type=ErrorType.RUNTIME,
        )
    finally:
        script_path.unlink(missing_ok=True)
