import time

def timer(func):
	"""A decorator that measures the execution time of a function."""
	def wrapper(*args, **kwargs):
		"""Inner function that wraps the decorated function."""
		start_time = time.time() # Record the start time
		result = func(*args, **kwargs) # Execute the original function
		end_time = time.time() # Record the end time
		execution_time = end_time - start_time
		print (f"Function {func.__name__} took {execution_time: .4f} seconds.")
		return result
	return wrapper

@timer
def my_function(a, b):
	"""A simple function that adds two numbers."""
	time.sleep(1) # Simulate some work
	return a + b

# Example usage
result = my_function(5, 3)
print (f"Result: {result}")
