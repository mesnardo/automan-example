"""
Example using the automation framework `automan`.
"""

import os
import pathlib
import urllib.request
import pandas
from matplotlib import pyplot
from automan.api import Problem, Simulation, Automator


class CpVsFoils(Problem):
  def get_name(self):
    return 'cp_vs_foils'

  def setup(self):
    cmd = ('python panelmethod.py')
    self.foils = ['naca0006-il', 'naca0010-il', 'naca0024-il',
                  'naca1408-il', 'naca1410-il', 'naca1412-il']
    self.cases = [Simulation(root=self.input_path(foil),
                             base_command=cmd,
                             input=os.path.join('foils', foil + '.dat'),
                             skiprows=1, n=100,
                             speed=1.0, alpha=0.0, method='source-vortex',
                             output=self.input_path(foil))
                  for foil in self.foils]

  def run(self):
    self.make_output_dir()
    self._plot_pressure_coefficient()

  def _plot_pressure_coefficient(self):
    print('[Figure 1] Reading data files ...')
    data = {}
    for foil in self.foils:
      filepath = os.path.join(self.input_path(foil), 'cp.txt')
      data[foil] = pandas.read_csv(filepath, sep='\t',
                                   names=['loc', 'x', 'cp'])
    print('[Figure 1] Plotting the surface pressure coefficient ...')
    fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
    ax.grid()
    ax.set_xlabel(r'$x$', fontsize=16)
    ax.set_ylabel(r'$C_p$', fontsize=16)
    color_cycle = ax._get_lines.prop_cycler
    for foil, subdata in data.items():
      color = next(color_cycle)['color']
      for loc, marker in zip(['lower', 'upper'], ['x', '|']):
        ax.plot(subdata[subdata['loc'] == loc]['x'],
                subdata[subdata['loc'] == loc]['cp'],
                label=f'{foil} ({loc})', color=color,
                linewidth=1.0, linestyle='-', marker=marker, markersize=4)
    ax.legend(prop={'size': 8}, ncol=3)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(1.0, -2.0)
    fig.tight_layout()
    print('[Figure 1] Saving figure ...')
    filepath = os.path.join(self.get_outputs()[0], 'figure1.png')
    fig.savefig(filepath, dpi=300, fmt='png')


class CpVsAngle(Problem):
  def get_name(self):
    return 'cp_vs_angle'

  def setup(self):
    cmd = ('python panelmethod.py')
    self.angles = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    self.foil = 'naca0006-il'
    self.cases = [Simulation(root=self.input_path(f'{self.foil}_{angle}'),
                             base_command=cmd,
                             input=os.path.join('foils', self.foil + '.dat'),
                             skiprows=1, n=100,
                             speed=1.0, alpha=angle, method='source-vortex',
                             output=self.input_path(f'{self.foil}_{angle}'))
                  for angle in self.angles]

  def run(self):
    self.make_output_dir()
    self._plot_pressure_coefficient()

  def _plot_pressure_coefficient(self):
    print('[Figure 2] Reading data files ...')
    data = {}
    for angle in self.angles:
      filepath = os.path.join(self.input_path(f'{self.foil}_{angle}'),
                              'cp.txt')
      data[angle] = pandas.read_csv(filepath, sep='\t',
                                    names=['loc', 'x', 'cp'])
    print('[Figure 2] Plotting the surface pressure coefficient ...')
    fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
    ax.grid()
    ax.set_xlabel(r'$x$', fontsize=16)
    ax.set_ylabel(r'$C_p$', fontsize=16)
    color_cycle = ax._get_lines.prop_cycler
    for angle, subdata in data.items():
      color = next(color_cycle)['color']
      ax.plot(subdata['x'], subdata['cp'],
              label=fr'{self.foil} - ($\alpha={angle}^o$)', color=color,
              linewidth=1.0, linestyle='-', marker='x', markersize=4)
    ax.legend(prop={'size': 8}, ncol=3)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(1.0, -10.0)
    fig.tight_layout()
    print('[Figure 2] Saving figure ...')
    filepath = os.path.join(self.get_outputs()[0], 'figure2.png')
    fig.savefig(filepath, dpi=300, fmt='png')


# Get foils data.
foils = ['naca0006-il', 'naca0010-il', 'naca0024-il',
         'naca1408-il', 'naca1410-il', 'naca1412-il']
output_dir = pathlib.Path().absolute() / 'foils'
output_dir.mkdir(parents=True, exist_ok=True)
for foil in foils:
  url = f'http://airfoiltools.com/airfoil/seligdatfile?airfoil={foil}'
  filepath = output_dir / (foil + '.dat')
  urllib.request.urlretrieve(url, filename=filepath)

automator = Automator(simulation_dir='data',
                      output_dir='manuscript/figures',
                      all_problems=[CpVsFoils, CpVsAngle])
automator.run()
