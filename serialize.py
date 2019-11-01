try:
    import cPickle as pickle
except ImportError:
    import pickle

def dump_obj(path, obj):
    f = file(path, 'wb')
    pickle.dump(obj, f)
    f.close()

def load_dump(path):
    f = file(path, 'rb')
    return pickle.load(f)
