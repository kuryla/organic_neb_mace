from ase.calculators.orca import ORCA, OrcaProfile
import argparse
from ase.io import read, write
import os
from ase.optimize import LBFGS
from ase import Atoms

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path to input configs", required=True)
    parser.add_argument("--ids", help="which configuration(s) to take", default="0")
    parser.add_argument("--output", help="path to save output configs to", required=True)
    parser.add_argument("--charge", help="charge", default=0, type=int)
    parser.add_argument("--mult", help="spin multiplicity", default=1, type=int)
    return parser.parse_args()

def get_calc(orca_path, charge=0, mult=1):
    calc = ORCA(
        profile=OrcaProfile(orca_path),
        label="orca",
        charge=charge, mult=mult,task='gradient',
        orcasimpleinput='RI-MP2 6-311G(d) autoaux nofrozencore TightSCF engrad',
        orcablocks='%pal nprocs 1 end \n %scf ConvForced=1 end'
    )
    return calc

def single_point(orca_path, config, charge, mult, prefix="mp2_"):
    calc = get_calc(orca_path, charge, mult)
    calc.calculate(atoms=config, properties={"energy", "forces"}, system_changes=None)
    os.system("rm orca_property.txt orca.*")
    config.info.update(
        {
            f"{prefix}energy": calc.results["energy"]
        }
    )
    config.arrays.update(
        {
            f"{prefix}forces": calc.results["forces"]
        }
    )
    return config

def optimize(config, charge, mult, out, fmax=0.01, nsteps=100):
    calc = get_calc(charge, mult)
    config.calc = calc
    opt = LBFGS(config)
    opt.run(fmax=fmax, steps=nsteps)
    write(out, opt.atoms)

def main():
    args = parse_args()
    configs = read(args.input, ":")

    if isinstance(configs, list):
        for config in configs:
            config = single_point(config, args.charge, args.mult)
        write(args.output, configs)
        os.system("rm orca.* orca_property.txt")

    elif isinstance(configs, Atoms):
        configs = single_point(configs, args.charge, args.mult)
        write(args.output, configs)
        os.system("rm orca.* orca_property.txt")

if __name__ == "__main__":
    main()
