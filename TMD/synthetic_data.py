"""
This module defines functions for generating synthetic data.

When ran, this module generates synthetic data, and it plots the data
in histograms.
"""

import numpy as np
import pandas as pd


def synth_data_for_point(mu, sigma, n=1):
    """
    Generate an array of n synthetic values based on mu and sigma.

    Args:
        mu: The center for the normal distribution.
        sigma: The deviation for the normal distribution.
        n: The number of values to be generated.

    Returns:
        An array of n random, normally-distributed values,
        where the distribution has mean mu and standard deviation sigma.
    """
    return np.array([np.random.normal(mu, sigma)
                     for _ in range(n)])


def synth_data_from_table(table, mu_key, sigma_key, n=1):
    """
    Generate a table of n synthetic values per row in table.

    Args:
        table: A pd.DataFrame object.
        mu_key: The index for the column of mu values.
                The mu values will be the means for the normal distributions.
        sigma_key: The index for the column of sigma values.
                   The sigma values will be the standard deviations for the
                   normal distributions.
        n: The number of synthetic values to generate per row in table.

    Returns:
        A pd.DataFrame object. Each row in the returned object will be a copy
        of a row in table, except the value at mu_key for that row will be
        replaced by a random, normally-distributed value.
        The normal distribution for that value has a mean based on the value
        at mu_key in the original row in table, and it has a standard deviation
        based on the the value at sigma_key for that row.
        The returned pd.DataFrame object will have be n-times as long as table.
    """
    synth_data = pd.DataFrame([])

    for i, row in table.iterrows():
        for _ in range(n):
            synth_point = row.copy()
            synth_point[mu_key] = np.random.normal(synth_point[mu_key],
                                                   synth_point[sigma_key])
            synth_data = synth_data.append(synth_point)

    return synth_data


if __name__ == '__main__':
    # NOTE: synth_data_for_point is tested when this is run.

    import matplotlib.pyplot as plt
    import our_lib
    import scipy.stats

    DATA = 'Dpp'
    N = 1000

    table = our_lib.tables[DATA]

    # Analyze the generated distribution for a single point.
    P = 0

    mu = table.get_value(P, 'exp_y')
    sigma = table.get_value(P, 'err')

    theor_cdf = scipy.stats.norm(mu, sigma).cdf

    #synth_data = synth_data_from_table(table, 'exp_y', 'err', N)
    synth_data = synth_data_for_point(mu, sigma, N)

    for n, bins in ((10, 6),
                    (100, 10),
                    (1000, 60)):

        #test_set = synth_data.get_value(P, 'exp_y')[:n]
        test_set = synth_data[:n]

        mean = np.mean(test_set)
        std_dev = np.std(test_set)
        exp_cdf = scipy.stats.norm(mean, std_dev).cdf

        # Plotting.
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.title('%d Synthetic Values Based on Point %d' % (n, P))
        plt.xlabel('Value')
        plt.ylabel('# of Values')

        vals, bins, patches = plt.hist(test_set, bins)

        step = bins[1] - bins[0]

        # Plot the normal distributions.
        # This can be done in different ways.
        x = np.arange(bins[0], bins[-1] + step, step)
        theor_y = (theor_cdf(x + step / 2) - theor_cdf(x - step / 2)) * n
        exp_y = (exp_cdf(x + step / 2) - exp_cdf(x - step / 2)) * n

        ax.plot(x, theor_y, 'r--', label='Theoretical')
        ax.plot(x, exp_y, 'g--', label='Actual')

        # Shrink the plot, and add a legend.
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Display the mean and standard deviation.
        plt.text(.2, .9, 'mean: %.4f\nstd_dev: %.4f' % (mean, std_dev),
                 ha='center', va='center', transform=ax.transAxes)

        #plt.savefig('plots\synth_values\%s_%d_values_point_%d.png'
        #            % (DATA, n, P))

        plt.show()

        plt.clf()