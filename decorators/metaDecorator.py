# -------------------------------- CAUTION -------------------------------------

# Please Dont do this it will haunt you every night, every time when you are alone
# it will make your life hell, make you dream scary shit but it won't kill you
# it will let you live but with fear and not a single courage to lookforward with this life

import ast
import inspect
import sys

def here_be_dragons(funct):  # create a decorator so we can, hm, enhance 'any' function
    def wrapper(*args, **kwargs):
        caller = inspect.getouterframes(inspect.currentframe())[1]  # pick up the caller
        parsed = ast.parse(caller[4][0], mode="single")  # parse the calling line
        arg_map = {}  # a map for our tracked args to establish global <=> local link
        for node in ast.walk(parsed):  # traverse the parsed code...
            # and look for a call to our wrapped function
            if isinstance(node, ast.Call) and node.func.id == funct.__name__:
                # loop through all positional arguments of the wrapped function
                for pos, var in enumerate(funct.func_code.co_varnames):
                    try:  # and try to find them in the captured call
                        if isinstance(node.args[pos], ast.Name):  # named argument!
                            arg_map[var] = node.args[pos].id  # add to our map
                    except IndexError:
                        break  # no more passed arguments
                break  # no need for further walking through the ast tree
        def trace(frame, evt, arg):  # a function to capture the wrapped locals
            if evt == "return":  # we're only interested in our function return
                for arg in arg_map:  # time to update our caller frame
                    caller[0].f_locals[arg_map[arg]] = frame.f_locals.get(arg, None)
        profile = sys.getprofile()  # in case something else is doing profiling
        sys.setprofile(trace)  # turn on profiling of the wrapped function
        try:
            return funct(*args, **kwargs)
        finally:
            sys.setprofile(profile)  # reset our profiling
    return wrapper


# Zap, there goes a pixie... Poor, poor, pixie. It will be missed.
@here_be_dragons
def your_function(in1, in2):
    in1 = in1 + 1
    in2 = in2 + 1