# A configuration registry gets populated once, and only once.
#  A piece of code uses one to allow its behaviour to be configured from outside.

import hello_world


hello_world.config["OUTPUT_FUNCTION"] = print


if __name__ == "__main__":
    hello_world.hello_world()

    
# The machinery in this case is simply a dictionary that is written to from outside the module.
# In a real world system, we might want a slightly more sophisticated config system (making it immutable for example, is a good idea).
# But at heart, any key-value store will do.