"""
Computes the surface pressure coefficient of an airfoil using a source-vortex
panel method.
"""

import os
import argparse
import aeropython


# Parse the command-line arguments.
formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser = argparse.ArgumentParser(description='Source-vortex panel method.')
parser.add_argument('--version', '-v',
                    action='version',
                    version='%(prog)s (version 0.1)')
parser.add_argument('--input', dest='input',
                    type=str, default=None,
                    help='Path of the file with airfoil coordinates.')
parser.add_argument('--skiprows', dest='skiprows',
                    type=int, default=0,
                    help='Number of rows to skip when reading coordinates.')
parser.add_argument('--n', '-n', dest='n',
                    type=int, default=40,
                    help='Number of panels to discretize airfoil.')
parser.add_argument('--naca', dest='naca_digits',
                    type=str, default=None,
                    help='The 4 digits of the NACA foil to be generated.')
parser.add_argument('--speed', dest='speed',
                    type=float, default=1.0,
                    help='Freestream speed.')
parser.add_argument('--alpha', dest='alpha',
                    type=float, default=0.0,
                    help='Freestream angle of incidence.')
parser.add_argument('--method', dest='method',
                    type=str, choices=['source', 'source-vortex'],
                    default='source-vortex',
                    help='Panel method to use.')
parser.add_argument('--output', dest='output',
                    type=str, default=os.getcwd(),
                    help='Output directory.')
args = parser.parse_args()

# Create the airfoil.
if args.naca_digits:
  x, y = aeropython.naca_generator(args.naca_digits, num=args.n, cusp=True)
  foil = aeropython.Airfoil(x=x, y=y)
else:
  foil = aeropython.Airfoil(filepath=args.input, skiprows=args.skiprows)
# Set the freestream conditions.
freestream = aeropython.Freestream(speed=args.speed, alpha=args.alpha)
foil.set_freestream(freestream)
# Discretize the geometry into panels.
foil.create_panels(N=args.n)
# Solve the panel method system.
foil.solve_panel_method(method=args.method)
# Compute the surface tangential velocity and pressure coefficient.
foil.compute_tangential_velocity()
foil.compute_pressure_coefficient()
# Write x-position, location on airfoil, and pressure coefficient into file.
if not os.path.isdir(args.output):
  os.makedirs(args.output)
filepath = os.path.join(args.output, 'cp.txt')
with open(filepath, 'w') as outfile:
  for p in foil.panels:
    outfile.write(f'{p.loc}\t{p.xc}\t{p.yc}\t{p.cp}\n')
