import time


def profile_and_print_result(func):
    start = time.time()
    result = func()
    end = time.time()

    print(f"Result => {result}. Time taken {end-start} (s)")