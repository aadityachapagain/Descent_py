import sys
import inspect

from sheep import Sheep


class Spare(object):
    '''
        This class will preserve the most fundamental works of 
        python codementality
    '''
    pass


class Container(Spare):
    '''
        This is the container to store all the useful information of
        python class that will be later useful
    '''

    def __init__(self, obj, docs):
        self.cls = obj
        self.docs = docs
        super().__init__()


if __name__ == "__main__":
    clsmembers = inspect.getmembers(sys.modules[__name__] , inspect.isclass)
    for clsname, obj in clsmembers:
        print(clsname,': ')
        print('\t',obj.__doc__)