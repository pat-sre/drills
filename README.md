# Drills

Personal tool for drilling algorithms, data structures, and ML. Self-hosted, local only.

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
| PyTorch | Basic training loop |

## Adding Exercises

### Structure

```
topic/
  new_algorithm/
    exercise.py   # Skeleton with function to implement
    solution.py   # Reference implementation
    tests.py      # Test suite with run_{func}_tests(func)
```

### Step-by-step

1. **Create the directory** under an existing topic (`sorting`, `graphs`, `trees`, `pytorch`):
   ```bash
   mkdir -p graphs/topological_sort
   ```

2. **Create `exercise.py`** with the function skeleton:
   ```python
   # Description of the problem.
   #
   # Explain input/output format.
   #
   def topo_sort(graph: dict[str, list[str]]) -> list[str]:
       pass


   if __name__ == "__main__":
       from tests import run_topo_sort_tests
       run_topo_sort_tests(topo_sort)
   ```

3. **Create `solution.py`** with your reference implementation (same structure, but implemented).

4. **Create `tests.py`**:
   ```python
   def run_topo_sort_tests(topo_sort):
       # Test 1: simple case
       graph = {"a": ["b"], "b": ["c"], "c": []}
       result = topo_sort(graph)
       assert result.index("a") < result.index("b") < result.index("c")

       # Test 2: ...
       
       print("All tests passed!")
   ```

### Naming conventions

The runner auto-derives function names:
- `sorting/*` → function is `sort`
- `*_first_search` → abbreviation (`bfs`, `dfs`)
- Otherwise → directory name is the function name

### Test locally

```bash
cd graphs/topological_sort
python exercise.py
```

The web UI auto-discovers new exercises on reload.
