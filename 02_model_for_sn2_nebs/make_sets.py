import numpy as np
from ase.io import read, write

indices = np.arange(1778)


ntrain = 1422
nvalid = 178
ntest = 178

np.random.seed(123)

train_id = np.random.choice(indices, size=ntrain, replace=False)
indices = np.setdiff1d(indices, train_id)
print(len(indices), len(train_id))

valid_id = np.random.choice(indices, size=nvalid, replace=False)
indices = np.setdiff1d(indices, valid_id)
print(len(indices), len(valid_id))

test_id = np.random.choice(indices, size=ntest, replace=False)
indices = np.setdiff1d(indices, test_id)
print(len(indices), len(test_id))


''' Generate train, valid, test sets for no rattle '''

e0s = read('./e0s.xyz', ':')

r_0 = read('./no-rattle/r-mp2.xyz', ':')
p_0 = read('./no-rattle/p-mp2.xyz', ':')
ts_0 = read('./no-rattle/ts-mp2.xyz', ':')



train = e0s \
      + [r_0[i] for i in train_id] \
      + [ts_0[i] for i in train_id] \
      + [p_0[i] for i in train_id]

valid = [r_0[i] for i in valid_id] \
      + [ts_0[i] for i in valid_id] \
      + [p_0[i] for i in valid_id]
    
test = [r_0[i] for i in test_id] \
      + [ts_0[i] for i in test_id] \
      + [p_0[i] for i in test_id]

write('./no-rattle/train.xyz', train)
write('./no-rattle/valid.xyz', valid)
write('./no-rattle/test.xyz', test)


''' Generate training set for stdev 0.02, use unrattled valid and test '''


r_rattled = read('./rattled-stdev-0.02/r-mp2.xyz', ':')
p_rattled = read('./rattled-stdev-0.02/p-mp2.xyz', ':')
ts_rattled = read('./rattled-stdev-0.02/ts-mp2.xyz', ':')


train = e0s \
      + [r_rattled[i] for i in train_id] \
      + [ts_rattled[i] for i in train_id] \
      + [p_rattled[i] for i in train_id]

valid = [r_0[i] for i in valid_id] \
      + [ts_0[i] for i in valid_id] \
      + [p_0[i] for i in valid_id]
    
test = [r_0[i] for i in test_id] \
      + [ts_0[i] for i in test_id] \
      + [p_0[i] for i in test_id]

write('./rattled-stdev-0.02/train.xyz', train)
write('./rattled-stdev-0.02/valid.xyz', valid)
write('./rattled-stdev-0.02/test.xyz', test)


''' Generate training set for stdev 0.05, use unrattled valid and test '''


r_rattled = read('./rattled-stdev-0.05/r-mp2.xyz', ':')
p_rattled = read('./rattled-stdev-0.05/p-mp2.xyz', ':')
ts_rattled = read('./rattled-stdev-0.05/ts-mp2.xyz', ':')


train = e0s \
      + [r_rattled[i] for i in train_id] \
      + [ts_rattled[i] for i in train_id] \
      + [p_rattled[i] for i in train_id]

valid = [r_0[i] for i in valid_id] \
      + [ts_0[i] for i in valid_id] \
      + [p_0[i] for i in valid_id]
    
test = [r_0[i] for i in test_id] \
      + [ts_0[i] for i in test_id] \
      + [p_0[i] for i in test_id]

write('./rattled-stdev-0.05/train.xyz', train)
write('./rattled-stdev-0.05/valid.xyz', valid)
write('./rattled-stdev-0.05/test.xyz', test)

write('r-test-mp2.xyz', [r_0[i] for i in test_id])
write('ts-test-mp2.xyz', [ts_0[i] for i in test_id])
write('p-test-mp2.xyz', [p_0[i] for i in test_id])