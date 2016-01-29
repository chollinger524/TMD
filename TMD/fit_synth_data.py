#!/usr/bin/python2

"""This script generates synthetic data, fits it, and plots it."""

from functools import partial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import our_lib
import residuals
import synthetic_data

N = 200 # N is number of data sets to be generated.
BINS = 14

p_indices = ('a1', 'a2', 'a3', 'a4', 'b')

parameters = pd.DataFrame(columns=p_indices)

start_p = (1.0, 1.0, 1.0, 1.0, 1.0)

# Generate and fit the synthetic data.
for i in range(N):
    # Generate the synthetic data. (4 tables are generated.)
    synth_tables = {}

    for k in ('Dpp', 'Dpm', 'Ppp', 'Ppm'):
        table = our_lib.tables[k]
        synth_tables[k] = (
            synthetic_data.synth_data_from_table(table, 'exp_y', 'err')
        )

    tables_funcs = [(synth_tables[k],
                     our_lib.theor_funcs[k]) for k in ('Dpp', 'Dpm', 'Ppp', 'Ppm')]

    # Fit the synthetic data.
    res_of_p = partial(residuals.res_array_from_tables, tables_funcs)

    opt_p = our_lib.leastsq(res_of_p, start_p)[0]

    # Save the parameters.
    parameters = parameters.append(pd.Series(dict(zip(p_indices, opt_p))),
                                   ignore_index=True)

    # Watch the time go by.
    print("%d / %d" % (i, N))

# Plot histograms of the parameters.
for p in p_indices:
    mean = np.mean(parameters[p])
    std_dev = np.std(parameters[p])

    plt.title(p)
    plt.xlabel('Value')
    plt.ylabel('# of Values')

    plt.hist(parameters[p], BINS)

    plt.text(.15, .9, 'mean: %.4f\nstd_dev: %.4f' % (mean, std_dev),
                 ha='center', va='center', transform=plt.gca().transAxes)

    #plt.savefig(r'plots\synth_parameters\%s.png' % p)

    plt.show()

    plt.clf()