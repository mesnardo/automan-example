"""
Example using the automation framework `automan`.
"""

import os
import pandas
from matplotlib import pyplot
from automan.api import Problem, Simulation, Automator


class CpVsFoils(Problem):
  def get_name(self):
    return 'cp_vs_foils'

  def setup(self):
    cmd = ('python panelmethod.py')
    self.naca_digits = ['0006', '0010', '0024', '1408', '1410', '1412']
    self.cases = [Simulation(root=self.input_path('naca' + digits),
                             base_command=cmd,
                             naca=digits, n=100,
                             speed=1.0, alpha=0.0, method='source-vortex',
                             output=self.input_path('naca' + digits))
                  for digits in self.naca_digits]

  def run(self):
    self.make_output_dir()
    self._plot_pressure_coefficient()

  def _plot_pressure_coefficient(self):
    print('[Figure 1] Reading data files ...')
    data = {}
    for digits in self.naca_digits:
      filepath = os.path.join(self.input_path('naca' + digits), 'cp.txt')
      data[digits] = pandas.read_csv(filepath, sep='\t',
                                     names=['loc', 'x', 'y', 'cp'])
    print('[Figure 1] Plotting surface pressure coefficients ...')
    fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
    ax.grid()
    ax.set_xlabel(r'$x$', fontsize=16)
    ax.set_ylabel(r'$C_p$', fontsize=16)
    color_cycle = ax._get_lines.prop_cycler
    for digits, subdata in data.items():
      color = next(color_cycle)['color']
      ax.plot(subdata[subdata['loc'] == 'upper']['x'],
              subdata[subdata['loc'] == 'upper']['cp'],
              label=f'NACA {digits}',
              color=color, linewidth=1.0, linestyle='-')
      ax.plot(subdata[subdata['loc'] == 'lower']['x'],
              subdata[subdata['loc'] == 'lower']['cp'],
              color=color, linewidth=1.0, linestyle='--')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::2], labels[::2], prop={'size': 10}, ncol=3)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(1.0, -1.0)
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
    self.naca_digits = '0012'
    self.cases = [Simulation(root=self.input_path('naca{}_{}'
                                                  .format(self.naca_digits,
                                                          angle)),
                             base_command=cmd,
                             naca=self.naca_digits, n=100,
                             speed=1.0, alpha=angle, method='source-vortex',
                             output=self.input_path('naca{}_{}'
                                                    .format(self.naca_digits,
                                                            angle)))
                  for angle in self.angles]

  def run(self):
    self.make_output_dir()
    self._plot_pressure_coefficient()

  def _plot_pressure_coefficient(self):
    print('[Figure 2] Reading data files ...')
    data = {}
    for angle in self.angles:
      filepath = os.path.join(self.input_path('naca{}_{}'
                                              .format(self.naca_digits,
                                                      angle)),
                              'cp.txt')
      data[angle] = pandas.read_csv(filepath, sep='\t',
                                    names=['loc', 'x', 'y', 'cp'])
    print('[Figure 2] Plotting surface pressure coefficients ...')
    fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
    ax.set_title(f'NACA {self.naca_digits}', fontsize=14)
    ax.grid()
    ax.set_xlabel(r'$x$', fontsize=16)
    ax.set_ylabel(r'$C_p$', fontsize=16)
    color_cycle = ax._get_lines.prop_cycler
    for angle, subdata in data.items():
      color = next(color_cycle)['color']
      ax.plot(subdata[subdata['loc'] == 'upper']['x'],
              subdata[subdata['loc'] == 'upper']['cp'],
              label=fr'$\alpha={angle}^o$',
              color=color, linewidth=1.0, linestyle='-')
      ax.plot(subdata[subdata['loc'] == 'lower']['x'],
              subdata[subdata['loc'] == 'lower']['cp'],
              color=color, linewidth=1.0, linestyle='--')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::2], labels[::2], prop={'size': 10}, ncol=1)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(1.0, -6.0)
    fig.tight_layout()
    print('[Figure 2] Saving figure ...')
    filepath = os.path.join(self.get_outputs()[0], 'figure2.png')
    fig.savefig(filepath, dpi=300, fmt='png')


automator = Automator(simulation_dir='data',
                      output_dir='manuscript/figures',
                      all_problems=[CpVsFoils, CpVsAngle])
automator.run()
