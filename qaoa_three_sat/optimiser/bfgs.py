"""
BFGS Optimizer Class

Author: Vivek Katial
"""

import numpy as np
from scipy.optimize import minimize


class BFGS:
    """This class is an Object for the BFGS Optimisation algorithm

    Attributes
    ----------
        vars : list
            A list of variables that need to be optimised (e.g. alpha_i and beta_i)
        cost_function : func
            A cost function with ``callback()`` that we're evaluating

    Example
    --------
    >>> from qaoa_three_sat.optimiser.nelder_mead import NelderMead
    >>> BFGS(vars_vec = [0,0], cost_function=rosen)
    >>> BFGS.optimise()
    """

    def __init__(self, vars_vec, cost_function, options=None):
        """
        Initialisation method on the class for rotations
        """
        self.vars_vec = vars_vec
        self.cost_function = cost_function
        self.options = options

    def optimise(self):
        """Optimisation Method for BFGS"""

        vars_vec_0 = self.vars_vec

        # Optimise alpha and beta using the cost function <s|H|s>
        res = minimize(self.cost_function, x0=vars_vec_0, method="BFGS")
