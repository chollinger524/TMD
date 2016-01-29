"""This module prepares the objects that are used in our research.

Attributes:
    tables: """

from functools import partial
import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import residuals

# Get the data.
tables = {'Dpp': pd.io.excel.read_excel('data\Dpp_unpol_Data.xlsx', header=0),
          'Dpm': pd.io.excel.read_excel('data\Dpm_unpol_Data.xlsx', header=0),
          'Ppp': pd.io.excel.read_excel('data\Ppp_unpol_Data.xlsx', header=0),
          'Ppm': pd.io.excel.read_excel('data\Ppm_unpol_Data.xlsx', header=0)}

# Modify table columns for compliance with res_array_of_table reqs.
for table in tables.values():
    table.columns = ['x', 'exp_y', 'err']

# Define theoretical functions for the different tables.
# For each of these functions, x is an array,
# and p is a sequence of parameters.
def _theor_dpp(x, p):
    return p[0] * 1.0 / ( np.pi * p[4] ) * np.exp( -x / p[4] )

def _theor_dpm(x, p):
    return p[1] * 1.0 / ( np.pi * p[4] ) * np.exp( -x / p[4] )

def _theor_ppp(x, p):
    return p[2] * 1.0 / ( np.pi * p[4] ) * np.exp( -x / p[4] )

def _theor_ppm(x, p):
    return p[3] * 1.0 / ( np.pi * p[4] ) * np.exp( -x / p[4] )

theor_funcs = {
    'Dpp': _theor_dpp,
    'Dpm': _theor_dpm,
    'Ppp': _theor_ppp,
    'Ppm': _theor_ppm
}

# Pair tables with funcs.
tables_funcs = [(tables[k], theor_funcs[k])
                for k in ('Dpp', 'Dpm', 'Ppp', 'Ppm')]

# Fit the tables.
res_of_p = partial(residuals.res_array_from_tables, tables_funcs)

start_p = (1.0, 1.0, 1.0, 1.0, 1.0)

opt_p = leastsq(res_of_p, start_p)[0]
r = res_of_p(opt_p)
opt_chi2 = np.dot(r, r)

# Remove unwanted variables from scope.
del table
del k
del r
