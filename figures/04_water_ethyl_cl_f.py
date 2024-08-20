from ase.io import read, write
import numpy as np
from matplotlib import pyplot as plt
import ase
from mace.calculators.mace import MACECalculator
from matplotlib.cm import get_cmap
from matplotlib import rc
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from PIL import Image

def d1_d2(config=ase.Atoms, n=int, l=int, c=int):
    pos = config.get_positions()
    d1 = np.linalg.norm(pos[c,:] - pos[n,:])
    d2 = np.linalg.norm(pos[c,:] - pos[l,:])
    return d1, d2

energies = np.zeros((2,40))
mp2_energies = np.zeros((2,40))
mp2_energies[0,:] = np.array([at.info['mp2_energy'] for at in read('../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter0/neb-mp2.xyz', ':')])
mp2_energies[1,:] = np.array([at.info['mp2_energy'] for at in read('../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter15/neb-mp2.xyz', ':')])
for i, iter in enumerate([0,15]):
    model = f'../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter{iter}/MACE_*_swa.model'
    calc = MACECalculator(model_paths=model, device='cpu', default_dtype='float64')
    neb = read(f'../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter{iter}/neb-mp2.xyz', ":")
    for j,atoms in enumerate(neb):
        calc.calculate(atoms=atoms)
        energies[i,j] = calc.results['energy']


s = 12
m = 18
l = 14

plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['legend.title_fontsize'] = 13

fig = plt.figure(layout='constrained', figsize=(12,10))

gs = GridSpec(10, 12, figure=fig)

ax1 = fig.add_subplot(gs[0:6, 0:6])
ax2 = fig.add_subplot(gs[0:6, 7:])

ax3 = fig.add_subplot(gs[6:10, 0:4])
ax4 = fig.add_subplot(gs[6:10, 4:8])
ax5 = fig.add_subplot(gs[6:10, 8:])

for ax in [ax3, ax4, ax5]:
    ax.set_xticks([])
    ax.set_yticks([])

display_mp2 = np.arange(16,32) #[0,2,4,6,7,8,9,10,11,12,13,15,17,19]

train_0 = read('../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter0/train.xyz', '5:')
d1d2 = np.array([list(d1_d2(atoms,  n=3, l=4, c=0)) for atoms in train_0])
d1 = d1d2[:,0]
d2 = d1d2[:,1]

#ax1.scatter(d2,d1, label='initial', marker='.')


cmap = get_cmap('viridis')
cm = [0.2+i/60 for i in range(30)]
cm.reverse()

ax1.set_ylim(1.4, 3.2)
ax1.set_xlim(1.4, 3.8)

lines = []

for i, c in zip([0,1,2,3,4,15], [0.8, 0.7, 0.6, 0.5, 0.4, 0.2]):
    neb = read(f'../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter{i}/neb.xyz', ':')
    d1d2 = np.array([list(d1_d2(atoms,  n=3, l=4, c=0)) for atoms in neb])
    d1 = d1d2[:,0]
    d2 = d1d2[:,1]
    if i != 15:
        ls = '--'
        alpha=0.7
    else:
        ls = 'solid'
        alpha=1
    lines += ax1.plot(d2,d1, label=f'AL iter {i}', zorder=0, c=cmap(c), ls=ls, alpha=alpha, marker='.')

for i in [1]:
    iter = [0, 15]
    cm = [0.8, 0.2]
    neb = read(f'../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter{iter[i]}/neb.xyz', ':')
    d1d2 = np.array([list(d1_d2(atoms,  n=3, l=4, c=0)) for atoms in neb])
    d1 = d1d2[:,0]
    d2 = d1d2[:,1]
    if iter[i] != 15:
        ls = '--'
        alpha=0.7
    else:
        ls = 'solid'
        alpha=1
    print(mp2_energies-energies[i,:])
    for im in display_mp2:
        ax2.plot([(d2-d1)[im]]*2, [energies[i, im] - np.min(energies[i,:]), mp2_energies[i, im] - np.min(mp2_energies[i,:])],c=cmap(cm[i]), zorder=0, linewidth=0.6, ls='dotted')
    ax2.plot((d2-d1), (energies[i,:] - np.min(energies[i,:])), c=cmap(cm[i]), ls=ls, alpha=alpha, zorder=0)
    ax2.scatter((d2-d1)[display_mp2], (mp2_energies[i,:] - np.min(mp2_energies[i,:]))[display_mp2], c=cmap(cm[i]), marker='D', s=12, zorder=1, label=f'MP2 AL iter {iter[i]}')

true_neb = np.array([at.get_potential_energy() for at in read('../ab-initio-neb/neb-run-from-neb1-lowest-im/neb-mp2.xyz', ':')])
true_neb -= np.min(true_neb)

d1d2 = np.array([list(d1_d2(atoms,  n=3, l=4, c=0)) for atoms in neb])
d1 = d1d2[:,0]
d2 = d1d2[:,1]
#ax2.plot(d2-d1, true_neb, c='red', marker='.')

ax1.set_ylabel('$d_1\ /\ \mathrm{\AA}$')
ax1.set_xlabel('$d_2\ /\ \mathrm{\AA}$')
ax1.axis("equal")
ax1.legend()

ax2.set_ylabel('Energy / eV')
ax2.set_xlabel('$d_2 - d_1 \ /\ \mathrm{\AA}$')


fname = "../nofrozencore/1-images-train60-highest-dis-std-0.02-2-models/iter15/train.xyz"
n_atom = 5
n_train = 60

configs = read(fname, ":")
initial = configs[n_atom : n_atom  + n_train]
neb_configs = configs[n_atom + n_train :]

d1i = []
d2i = []

for c in initial:
    d1, d2 = d1_d2(c, n=3, l=4, c=0)
    d1i.append(d1)
    d2i.append(d2)

d1n = []
d2n = []

for c in neb_configs:
    d1, d2 = d1_d2(c, n=3, l=4, c=0)
    d1n.append(d1)
    d2n.append(d2)

s1 = ax1.scatter(d2i, d1i, label="Initial data", marker=".")
s2 = ax1.scatter(d2n, d1n, label="NEB", marker="D", c='red', s=12)


ax1.legend()
ax1.set_aspect('equal')
ax1.set_ylabel('$d_1\ /\ \mathrm{\AA}$')
ax1.set_xlabel('$d_2\ /\ \mathrm{\AA}$')
ax2.legend()



legend1 = ax1.legend(handles=lines, loc=1, title='NEB pathways')
ax1.add_artist(legend1)
#legend2 = ax1.legend(handles=[s1], loc=5, title='Training data')
legend2 = ax1.legend(handles=[s1,s2], loc=9, title='Training data')

img = np.asarray(Image.open('../../figures/r.png'))
ax3.imshow(img)
ax3.set_title('Reactants')
img = np.asarray(Image.open('../../figures/ts.png'))
ax4.imshow(img)
ax4.set_title('Transition state')
img = np.asarray(Image.open('../../figures/p.png'))
ax5.imshow(img)
ax5.set_title('Products')

ax3.plot([0.3, 0.45], [0.48, 0.43], transform=ax3.transAxes, linewidth=2, color='#666666', ls='--')
ax4.plot([0.32, 0.4], [0.44, 0.42], transform=ax4.transAxes, linewidth=2, color='#666666', ls='--')
ax4.plot([0.52, 0.6], [0.42, 0.44], transform=ax4.transAxes, linewidth=2, color='#666666', ls='--')
ax5.plot([0.47, 0.63], [0.41, 0.46], transform=ax5.transAxes, linewidth=2, color='#666666', ls='--')

plt.tight_layout()
plt.savefig('../figures/solv-neb.pdf')
