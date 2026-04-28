from functools import wraps


def limit_args(max_value, mode):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if mode == "clip":
                new_args = [
                    min(arg, max_value) if isinstance(arg, (int, float)) else arg
                    for arg in args
                ]
                return func(*new_args, **kwargs)
            elif mode == "error":
                for arg in args:
                    if isinstance(arg, (int, float)) and arg > max_value:
                        raise ValueError(f"Argument {arg} is greater than {max_value}")
                return func(*args, **kwargs)

        return wrapper

    return actual_decorator


@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b


print(multiply(2, 3))
print(multiply(100, 3))
