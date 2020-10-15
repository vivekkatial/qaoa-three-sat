"""
Nelder-Mead Optimizer Class

Author: Vivek Katial
"""

import numpy as np
from scipy.optimize import minimize


class NelderMead:
    """This class is an Object for the Nelder-Mead Optimisation algorithm

    Attributes
    ----------
        vars : list
            A list of variables that need to be optimised (e.g. alpha_i and beta_i)
        cost_function : func
            A cost function with ``callback()`` that we're evaluating
        options : dict
            Optimisation Algorithm Parameters Dictionary.

    Example
    --------
    >>> from qaoa_three_sat.optimiser.nelder_mead import NelderMead
    >>> NelderMead(vars_vec = [0,0], cost_function=rosen, options=opts_dict)
    >>> NelderMead.optimise()
    """

    def __init__(self, vars_vec, cost_function, options):
        """
        Initialisation method on the class for rotations
        """
        self.vars_vec = vars_vec
        self.cost_function = cost_function
        self.options = options

    def optimise(self):
        """Optimisation Method for Nelder-Mead"""
        # Build a simplex (add epsilon to alpha / add epsilon to beta)
        vars_vec_0 = self.vars_vec

        # Optimise alpha and beta using the cost function <s|H|s>
        res = minimize(
            self.cost_function,
            x0=vars_vec_0,
            method="nelder-mead",
            options={
                "xtol": self.options["xtol"],
                "disp": self.options["disp"],
                "adaptive": self.options["adaptive"],
            },
        )

        # Print result
        print(
            "Optimal Sol:\t alpha:%s beta:%s"
            % (
                res.x[0 : (int(len(self.vars_vec) / 2))],
                res.x[int(len(self.vars_vec) / 2) :],
            )
        )
        self.vars_vec = res.x
