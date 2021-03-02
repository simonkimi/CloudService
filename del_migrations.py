import os
import re

for root, dirs, files in os.walk('./apps'):
    for file in files:
        path = os.path.join(root, file)
        if 'migrations' in path and re.search(r'\d{4}.+py', path):
            os.remove(path)


