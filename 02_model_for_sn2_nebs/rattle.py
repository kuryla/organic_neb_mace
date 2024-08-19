from ase.io import read, write
import os

reactants = read('r/r-opt.xyz', ':')
products = read('p/p-opt.xyz', ':')
t_states = read('ts/ts-selected.xyz', ':')

''' no-rattle '''

if not os.path.exists('no-rattle'):
    os.system('mkdir no-rattle')

write('no-rattle/r.xyz', reactants)
write('no-rattle/p.xyz', products)
write('no-rattle/ts.xyz', t_states)

''' stdev 0.02 '''

r2 = []
p2 = []
ts2 = []

seed = 0

for at in reactants:
    at2 = at.copy()
    at2.rattle(stdev=0.02, seed=seed)
    r2.append(at2)
    seed += 1

for at in products:
    at2 = at.copy()
    at2.rattle(stdev=0.02, seed=seed)
    p2.append(at2)
    seed += 1

for at in t_states:
    at2 = at.copy()
    at2.rattle(stdev=0.02, seed=seed)
    ts2.append(at2)
    seed  += 1

if not os.path.exists('rattled-stdev-0.02'):
    os.system('mkdir rattled-stdev-0.02')

write('./rattled-stdev-0.02/r.xyz', r2)
write('./rattled-stdev-0.02/p.xyz', p2)
write('./rattled-stdev-0.02/ts.xyz', ts2)

''' stdev 0.05 '''

r3 = []
p3 = []
ts3 = []

for at in reactants:
    at2 = at.copy()
    at2.rattle(stdev=0.05, seed=seed)
    r3.append(at2)
    seed  += 1

for at in products:
    at2 = at.copy()
    at2.rattle(stdev=0.05, seed=seed)
    p3.append(at2)
    seed  += 1

for at in t_states:
    at2 = at.copy()
    at2.rattle(stdev=0.05, seed=seed)
    ts3.append(at2)
    seed  += 1
    
if not os.path.exists('rattled-stdev-0.05'):
    os.system('mkdir rattled-stdev-0.05')

write('./rattled-stdev-0.05/r.xyz', r3)
write('./rattled-stdev-0.05/p.xyz', p3)
write('./rattled-stdev-0.05/ts.xyz', ts3)