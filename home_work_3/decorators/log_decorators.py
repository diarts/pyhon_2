def function_log(logger, main_func_name: str):
    def main_wrapper(func):
        def wrapper(*args, **kwargs):
            logger.debug(f'function {func.__name__} call from function {main_func_name}')
            result = func(*args, **kwargs)
            logger.debug(f'function {func.__name__} completed execution and return {result}')
            return result

        return wrapper

    return main_wrapper


if __name__ == '__main__':
    import inspect


    def foo():
        print(inspect.getframeinfo(inspect.currentframe().f_back)[2])


    def foo2():
        foo()


    foo()
    foo2()
