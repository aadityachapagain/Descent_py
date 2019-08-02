# First Lets create a simple decorator which will add or change the functionality of function

import time
from functools import wraps

def logger(func):
    def wrapper(*args, **kwargs):
        # lets do function introsectpion
        print('Inside Function: ',func.__name__)
        print('--------------------------------')
        return func(*args, **kwargs)
    return wrapper


# lets call that function using logger
@logger
def gretting(name):
    print(f'grettings to the legend: {name}')
    # some complex task
    time.sleep(0.5)
    return 'results'

# Now just you implemented the decorator to put logger easily but do you really must trust the decorator
# No , it might do something unwanted inside it
# beaware

# after using decorater the one you looking for might not be the same at all

'''
Lets go to the python interactive shell gaze upon the identity of our real function

>>> gretting.__name__
'wrapper'
>>> gretting
<function logger.<locals>.wrapper at 0x7f1e989a6510>

'''

# This is the big problem in if we implment decorator in real world
# How to solve that well just import wraps from functools and 
# wrap the wrapper with @wraps and you are  good to go in real world 
# Example Below

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # lets do function introsectpion
        print('Inside Function: ',func.__name__)
        print('--------------------------------')
        return func(*args, **kwargs)
    return wrapper


# lets call that function using logger
@logger
def greet(name):
    print(f'greet to the legend: {name}')
    # some complex task
    time.sleep(0.5)
    return 'results'