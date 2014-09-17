_objs = []
_dict = {}

def add(obj, name=None):
    _objs.append(obj)
    if name:
        _dict[name] = obj

def get(name):
    return _dict[name]
