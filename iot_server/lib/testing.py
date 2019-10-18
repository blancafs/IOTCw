import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from engine import Engine
from configuration import TEST_STRINGS


engine = Engine()
test = ['stamp,seq,' + x for x in TEST_STRINGS]
for i in test:
    print(engine.dealWithData(i))
