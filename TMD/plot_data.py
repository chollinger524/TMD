#!/usr/bin/python2

"""Plot the JLab data with the theoretical functions."""

import matplotlib.pyplot as plt
from our_lib import *


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
    subplots[i].plot(tables[h]['x'].values,
        theor_funcs[h](tables[h]['x'].values, opt_p),
        'b-', linewidth=2)

    subplots[i].errorbar(tables[h]['x'].values,
        tables[h]['exp_y'].values,
        tables[h]['err'].values,
        fmt='o', ecolor='r', markerfacecolor='r')

for sp in subplots:
    figure.add_subplot(sp)

figure.tight_layout()

if SAVE:
    figure.savefig('plots\Mason_plot.pdf')