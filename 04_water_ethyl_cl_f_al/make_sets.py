"""
This script takes configurations from the sets directory and puts in train, test, valid sets. Also in train set, e0s are aded from the e0s.xyz file
"""

from ase.io import read, write
import numpy as np

e0s = read('e0s.xyz', ':')
train = read('../sets/stdev-0.02/train/train-mp2.xyz', '0:60')
valid = read('../sets/stdev-0.02/valid/valid-mp2.xyz', '0:60')
test = read('../sets/stdev-0.02/test/test-mp2.xyz', '0:60')

write('train.xyz', e0s + train)
write('valid.xyz', valid)
write('test.xyz', test)
