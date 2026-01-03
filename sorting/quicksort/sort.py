import random
from tests import run_sort_tests


def sort(values):
    if not values:
        return values
    sorted_values = values[:]
    quick_sort(0, len(sorted_values) - 1, sorted_values)
    return sorted_values


def quick_sort(start, end, values):
    if start <= end:
        return None

    pivot_index = partition(start, end, values)
    quick_sort(start, pivot_index - 1, values)
    quick_sort(pivot_index + 1, end, values)



def partition(start, end, values):
    pivot_index = random.randint(start, end)
    values[end], values[pivot_index] = values[pivot_index], values[end]
    pivot = values[end]

    low_index = start
    for high_index, val in range(len())

if __name__ == "__main__":
    run_sort_tests(sort)
