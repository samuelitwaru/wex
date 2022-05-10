def range_with_floats(start, stop, step=1):
    while stop > start:
        yield start
        start += step
    