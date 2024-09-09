import sys,os

sys.path.append(f"{os.getcwd()}")

from game.asset.conv import Identification
from enum import Enum

class TESTS(Enum):
    i1 = Identification()
    i2 = Identification()

i2c = TESTS.i1

print(i2c in TESTS._member_map_.values())

print([Identification(),Identification()])