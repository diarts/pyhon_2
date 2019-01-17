import inspect


def function_log(logger):
    def main_wrapper(func):
        def wrapper(*args, **kwargs):
            logger.debug(f'function {func.__name__} call from function {inspect.stack()[1][3]}')
            result = func(*args, **kwargs)
            logger.debug(f'function {func.__name__} completed execution and return {result}')
            return result

        return wrapper

    return main_wrapper


if __name__ == '__main__':
    def foo():
        print(inspect.getframeinfo(inspect.currentframe().f_back)[2])


    def foo2():
        foo()


    foo()
    foo2()
