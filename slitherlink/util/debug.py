def timeit(func):
    import time

    def timeit_wrap(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'{func.__name__} took {time.perf_counter()-start} seconds')
        return result
    return timeit_wrap


def profile(func):
    from pyinstrument import Profiler

    def wrapper(*args, **kwargs):
        profiler = Profiler()
        profiler.start()

        result = func(*args, **kwargs)

        profiler.stop()
        filename = 'profile.html'  # You can change this if needed
        with open(filename, 'w') as f:
            f.write(profiler.output_html())

        return result
    return wrapper
