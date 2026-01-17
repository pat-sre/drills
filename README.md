# Drills

Practice algorithms, data structures, and ML concepts through implementation exercises.

## Usage

```bash
python run.py                     # List topics
python run.py attention           # List exercises in topic
python run.py attention 01        # Run exercise
python run.py attention 01 -s     # Run solution
```

## Structure

```
topic/
  01_exercise_name/
    exercise.py   # Skeleton to implement
    solution.py   # Reference implementation
    tests.py      # Test suite
```

## Topics

| Topic | Exercises |
|-------|-----------|
| `dsa1_sorting` | Insertion sort, Merge sort, Quicksort |
| `dsa2_trees` | DFS, BFS |
| `dsa3_graphs` | BFS, DFS, Dijkstra |
| `ml1_pytorch` | Training loops, DataLoaders |
| `ml2_attention` | Scaled dot-product, Causal attention, Self-attention, Multi-head |
| `ml3_lora` | LoRA basics, LLM fine-tuning, JSONL chat, GGUF export |

## Adding Exercises

1. Create directory under a topic:
   ```bash
   mkdir -p dsa3_graphs/04_topological_sort
   ```

2. Create `exercise.py` with just the function:
   ```python
   def topo_sort(graph: dict[str, list[str]]) -> list[str]:
       pass
   ```

3. Create `solution.py` with reference implementation.

4. Create `tests.py`:
   ```python
   from test_utils import run_all

   def run_tests(topo_sort):
       tests = [
           {
               "name": "linear chain",
               "func": topo_sort,
               "inputs": {"graph": {"a": ["b"], "b": ["c"], "c": []}},
               "check": lambda r: r.index("a") < r.index("b") < r.index("c"),
               "fail_msg": "a should come before b before c",
           },
       ]
       run_all("topo_sort", tests)
   ```
