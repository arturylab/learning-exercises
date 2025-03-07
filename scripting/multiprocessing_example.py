'''
This script compares the performance of calculating Fibonacci numbers 
using different parallelism techniques.
'''

import time
import concurrent.futures

def fibonacci(n):
    """Recursive Fibonacci calculation (inefficient on purpose)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def without_parallelism(numbers):
    """Calculate Fibonacci numbers without parallelism."""
    return [fibonacci(n) for n in numbers]

def with_threading(numbers):
    """Calculate Fibonacci numbers using ThreadPoolExecutor (not effective for CPU-bound tasks)."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(executor.map(fibonacci, numbers))

def with_multiprocessing(numbers):
    """Calculate Fibonacci numbers using ProcessPoolExecutor (should improve performance)."""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return list(executor.map(fibonacci, numbers))

def measure_time(func, numbers, label):
    """Measure the execution time of a function."""
    start = time.perf_counter()
    func(numbers)
    end = time.perf_counter()
    print(f"{label}: {end - start:.4f} seconds")

if __name__ == "__main__":
    numbers = [35, 36, 37, 38, 39, 40]  # CPU-intensive tasks (Fibonacci of these numbers)

    measure_time(without_parallelism, numbers, "Without parallelism")
    measure_time(with_threading, numbers, "With ThreadPoolExecutor")
    measure_time(with_multiprocessing, numbers, "With ProcessPoolExecutor")