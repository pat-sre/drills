# Drills

A personal practice tool for algorithm and data structure implementations. Write code, run tests, track progress.

## Quick Start

```bash
pip install fastapi uvicorn
uvicorn web.app:app --reload
```

Open http://localhost:8000

## How It Works

1. Select an exercise from the sidebar
2. Implement the function in the editor
3. Submit to run tests
4. Track your pass count over time

Each exercise has a skeleton (`exercise.py`), reference solution (`solution.py`), and test suite.

## CLI

Run exercises directly:

```bash
python -m sorting.insertion_sort.exercise
```

## Topics

| Category | Exercises |
|----------|-----------|
| Sorting | Insertion sort, Merge sort, Quicksort |
| Graphs | BFS, DFS, Dijkstra |
| Trees | BFS, DFS |

## Adding Exercises

Create a new directory under a topic:

```
topic/
  new_algorithm/
    exercise.py   # Skeleton with function to implement
    solution.py   # Reference implementation
    tests.py      # Test suite with run_{func}_tests(func)
```

The web UI auto-discovers new exercises on reload.
