import pickle

def write_pickle(filepath, object):
    with open(filepath, 'wb') as fp:
        pickle.dump(object, fp)


def read_pickle(filepath):
    with open(filepath, 'rb') as f:  # notice the r instead of w
        pickled_object = pickle.load(f)
    return pickled_object