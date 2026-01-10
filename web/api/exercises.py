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


def _derive_func_name(topic: str, name: str) -> str:
    """Derive function name from exercise name using conventions."""
    # Sorting always uses 'sort'
    if topic == "sorting":
        return "sort"

    # Search algorithms use abbreviations
    if name.endswith("_first_search"):
        # breadth_first_search -> bfs, depth_first_search -> dfs
        return "".join(word[0] for word in name.split("_"))

    # Default: use exercise name as-is
    return name


def get_test_config(topic: str, name: str) -> dict[str, str]:
    """Auto-derive test configuration from naming conventions."""
    func_name = _derive_func_name(topic, name)

    # Sorting uses topic-level tests
    if topic == "sorting":
        return {
            "func_name": func_name,
            "test_import": "from sorting.tests import run_sort_tests",
            "test_call": "run_sort_tests(sort)",
        }

    # Other topics use per-exercise tests
    return {
        "func_name": func_name,
        "test_import": f"from {topic}.{name}.tests import run_{func_name}_tests",
        "test_call": f"run_{func_name}_tests({func_name})",
    }
