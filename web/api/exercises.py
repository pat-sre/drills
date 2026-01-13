import re
from pathlib import Path

from .config import PROJECT_ROOT, TOPICS


def discover_exercises() -> dict[str, list[str]]:
    """Scan topics for exercises. Returns {topic: [exercise_name, ...]}."""
    result: dict[str, list[str]] = {}

    for topic in TOPICS:
        topic_path = PROJECT_ROOT / topic
        if not topic_path.exists():
            continue

        exercises = []
        for exercise_dir in sorted(topic_path.iterdir()):
            if exercise_dir.is_dir() and (exercise_dir / "exercise.py").exists():
                exercises.append(exercise_dir.name)

        if exercises:
            result[topic] = exercises

    return result


def get_exercise_path(topic: str, name: str) -> Path:
    """Get path to exercise.py file."""
    return PROJECT_ROOT / topic / name / "exercise.py"


def get_exercise_code(topic: str, name: str) -> str | None:
    """Read exercise skeleton code. Returns None if not found."""
    path = get_exercise_path(topic, name)
    if not path.exists():
        return None
    return path.read_text()


def _discover_func_name(exercise_path: Path) -> str | None:
    """Discover the main function name from an exercise file."""
    if not exercise_path.exists():
        return None
    content = exercise_path.read_text()
    match = re.search(r"^def (\w+)\(", content, re.MULTILINE)
    if match:
        return match.group(1)
    return None


def get_test_config(topic: str, name: str) -> dict[str, str]:
    """Get test configuration for an exercise."""
    # Discover function name from exercise file
    exercise_path = PROJECT_ROOT / topic / name / "exercise.py"
    func_name = _discover_func_name(exercise_path) or name

    # Sorting uses topic-level tests
    if topic == "sorting":
        return {
            "func_name": func_name,
            "test_import": "from sorting.tests import run_tests",
            "test_call": f"run_tests({func_name})",
        }

    return {
        "func_name": func_name,
        "test_import": f"from {topic}.{name}.tests import run_tests",
        "test_call": f"run_tests({func_name})",
    }
