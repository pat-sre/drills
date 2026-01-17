#!/usr/bin/env python3
"""
Run exercises.

Usage:
    python run.py                     # List all topics
    python run.py attention           # List exercises in topic
    python run.py attention 01        # Run exercise
    python run.py attention 01 -s     # Run solution
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def find_topics():
    """Find all topic directories."""
    return sorted(
        d.name
        for d in ROOT.iterdir()
        if d.is_dir()
        and not d.name.startswith((".", "_"))
        and any(d.glob("*/exercise.py"))
    )


def find_exercises(topic_query):
    """Find topic matching query and its exercises."""
    topics = find_topics()

    matches = [t for t in topics if topic_query.lower() in t.lower()]
    if not matches:
        print(f"No topic matching '{topic_query}'")
        print(f"Available: {', '.join(topics)}")
        sys.exit(1)
    if len(matches) > 1:
        exact = [t for t in matches if topic_query.lower() == t.lower()]
        if len(exact) == 1:
            matches = exact
        else:
            print(f"Multiple topics match '{topic_query}': {', '.join(matches)}")
            sys.exit(1)

    topic = matches[0]
    topic_dir = ROOT / topic

    exercises = sorted(
        d.name
        for d in topic_dir.iterdir()
        if d.is_dir() and (d / "exercise.py").exists()
    )

    return topic, exercises


def run_exercise(topic, exercise_name, solution=False):
    """Run an exercise or solution."""
    file_type = "solution" if solution else "exercise"

    try:
        module = importlib.import_module(f"{topic}.{exercise_name}.{file_type}")
        tests = importlib.import_module(f"{topic}.{exercise_name}.tests")
    except ModuleNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    tests.run_tests(module.solve)


def main():
    args = sys.argv[1:]

    if not args:
        topics = find_topics()
        print("Topics:")
        for t in topics:
            print(f"  {t}")
        print(f"\nUsage: python run.py <topic> [exercise] [-s]")
        return

    solution = "-s" in args
    args = [a for a in args if a != "-s"]

    topic_query = args[0]
    topic, exercises = find_exercises(topic_query)

    if len(args) == 1:
        print(f"{topic}:")
        for ex in exercises:
            print(f"  {ex}")
        print(f"\nUsage: python run.py {topic_query} <exercise> [-s]")
        return

    ex_query = args[1]
    matches = [e for e in exercises if ex_query in e]
    if not matches:
        print(f"No exercise matching '{ex_query}' in {topic}")
        print(f"Available: {', '.join(exercises)}")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Multiple exercises match '{ex_query}': {', '.join(matches)}")
        sys.exit(1)

    run_exercise(topic, matches[0], solution)


if __name__ == "__main__":
    main()
