"""This module defines several functions that return arrays of residuals."""

import numpy as np


def res_array(exp, theor, err):
    """
    Return the residual or an array of the residuals for the arguments.

    The arguments should either all be single values or all be n-d arrays.

    Args:
        exp: An experimental value or an array of values.
        theor: A theoretical value or an array of theoretical values.
        err: An error value or an array of error values.
    """
    return (exp - theor) / err


def res_array_of_table(table, theor_func, f_arg):
    """
    Return an array of the residuals for the given arguments.

    The values in the table are used to calculate the residuals.
    theor_func is applied to the values of the 'x' column of the table along
    with f_arg to evaluate the theoretical values to be used in the
    calculations.

    Args:
        table: A pd.DataFrame object with columns ['x', 'exp_y', 'err'].
        theor_func: A function with two parameters.
                    The function must accept an np.array for the first
                    argument.
                    The function must accept p as the second argument.
        f_arg: The additional parameter(s) to be passed to theor_func.
    """
    if ('x' not in table.columns
        or 'exp_y' not in table.columns
        or 'err' not in table.columns):
        raise ValueError("table must have columns ['x', 'exp_y', 'err'].")
    return res_array(table['exp_y'].values,
                     theor_func(table['x'].values, f_arg),
                     table['err'].values)


def res_array_from_tables(table_func_pairs, f_arg):
    """
    Return an array of all of the residuals from the tables and functions.

    Each function in table_func_pairs is applied to the values of its
    corresponding table's 'x' column. The results are used in the calculations
    of the residuals along with the values of the table's 'exp_y' and 'err'
    columns.

    Args:
        table_func_pairs: A sequence of (table, function) pairs.
                          The tables are pd.DataFrame objects.
                          The tables have columns ['x', 'exp_y', 'err'].
                          The functions must each accept two arguments.
                          The functions must each accept an np.array for their
                          first arguments.
                          The functions must each accept p for their second
                          arguments.
        f_arg: The additional argument to be passed to each of the functions.
    """
    r = np.array([])
    for table, func in table_func_pairs:
        r = np.append(r, res_array_of_table(table, func, f_arg))
    return r
