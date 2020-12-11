try:
    number_type = int, long
except NameError:
    number_type = int

try:
    iter_range = xrange
except NameError:
    iter_range = range
