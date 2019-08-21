# It is portal which will generate child data

# Now create a Class just to store a data statically

class DataStorage:
    _info = {'default':'This is for test'}
    _obj = None

    def __new__(cls, *args, **kargs):
        if cls._obj:
            print('already contain Obj ...')
            return cls._obj
        else:
            instance = super(DataStorage, cls).__new__(cls, *args, **kargs)
            cls._obj = instance
            return instance

def generate_info(args, info):
    if args == 'clean':
        if type(info) == dict:
            DataStorage()._info = info
        else:
            raise TypeError("Need type of Dict")
    else:
        if type(info) == dict:
            DataStorage()._info.update(info)
        else:
            raise TypeError("Need type of Dict")


def get_info():
    return DataStorage()._info