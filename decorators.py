from functools import wraps


class Decorator:
    """
    Stores reusable decorators for console output
    and safe database operations.
    """

    @staticmethod
    def frame(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("=" * 50)

            result = func(*args, **kwargs)

            print("=" * 50)
            return result

        return wrapper

    @staticmethod
    def handle_errors(errors, default_return=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except errors as error:
                    print(f"Error: {error}")
                    return default_return

            return wrapper

        return decorator