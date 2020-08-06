import pickle

with open('badpickle.p', 'rb') as fh:
    pick = pickle.load(fh)
