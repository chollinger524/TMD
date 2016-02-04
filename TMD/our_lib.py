"""
This module prepares the objects that are used in our research.

tables: A dict with keys ['Dpp', 'Dpm', 'Ppp', 'Ppm'] mapped to
       pd.DataFrame objects with columns ['x', 'exp_y', 'err'].
theor_funcs: A dict with keys ['Dpp', 'Dpm', 'Ppp', 'Ppm'].
             The keys are mapped to functions.
             The functions take args x and p:
                 x: A numerical value or an array.
                 p: A sequence of parameters.
tables_funcs: A list of the pd.DataFrame objects in tables and the functions
              in theor_funcs paired together by key.
res_of_p: A function of one arg, p.
          p must be a sequence of 5 parameters.
          Returns an array of the residuals determined by the data and
          functions in tables_funcs when p is passed to the functions in
          table_funcs.
start_p: The initial sequence of parameters passed to the leastsq optimization.
opt_p: The optimized sequence of parameters.
opt_chi2: The chi^2 value based on the residuals calculated with opt_p.
"""

from functools import partial
import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import residuals

# Get the data.
tables = {'Dpp': pd.io.excel.read_excel('data/Dpp_unpol_Data.xlsx', header=0),
          'Dpm': pd.io.excel.read_excel('data/Dpm_unpol_Data.xlsx', header=0),
          'Ppp': pd.io.excel.read_excel('data/Ppp_unpol_Data.xlsx', header=0),
          'Ppm': pd.io.excel.read_excel('data/Ppm_unpol_Data.xlsx', header=0)}

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
