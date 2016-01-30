#!/usr/bin/python2

"""Plot the JLab data with the theoretical functions."""

import matplotlib.pyplot as plt
import our_lib

SAVE = False

# subplots will be for Dpp, Dpm, Ppp, Ppm (in that order).
figure = plt.figure()
subplots = []

subplots.append(plt.subplot(2, 2, 1,
    title='$\mathrm{\gamma^* + D \longrightarrow \pi^+ + X}$',
    xlabel='$\mathrm{P_{hT}^2 (GeV^2)}$',
    ylabel='$\mathrm{d\sigma/d P_{hT}^2}$',
    ylim=(3.e-1, 4.e+0),
    yscale='log'))

subplots.append(plt.subplot(2, 2, 2,
    title='$\mathrm{\gamma^* + D \longrightarrow \pi^- + X}$',
    xlabel='$\mathrm{P_{hT}^2 (GeV^2)}$',
    ylabel='$\mathrm{d\sigma/d P_{hT}^2}$',
    ylim=(3.e-1, 4.e+0),
    yscale='log'))

subplots.append(plt.subplot(2, 2, 3,
    title='$\mathrm{\gamma^* + P \longrightarrow \pi^+ + X}$',
    xlabel='$\mathrm{P_{hT}^2 (GeV^2)}$',
    ylabel='$\mathrm{d\sigma/d P_{hT}^2}$',
    ylim=(1.e-1, 4.e+0),
    yscale='log'))

subplots.append(plt.subplot(2, 2, 4,
    title='$\mathrm{\gamma^* + P \longrightarrow \pi^- + X}$',
    xlabel='$\mathrm{P_{hT}^2 (GeV^2)}$',
    ylabel='$\mathrm{d\sigma/d P_{hT}^2}$',
    ylim=(1.e-1, 4.e+0),
    yscale='log'))

for i, h in enumerate(('Dpp', 'Dpm', 'Ppp', 'Ppm')):
    subplots[i].plot(our_lib.tables[h]['x'].values,
        our_lib.theor_funcs[h](our_lib.tables[h]['x'].values, our_lib.opt_p),
        'b-', linewidth=2)

    subplots[i].errorbar(our_lib.tables[h]['x'].values,
        our_lib.tables[h]['exp_y'].values,
        our_lib.tables[h]['err'].values,
        fmt='o', ecolor='r', markerfacecolor='r')

for sp in subplots:
    figure.add_subplot(sp)

figure.tight_layout()

if SAVE:
    figure.savefig('plots/Mason_plot.pdf')
