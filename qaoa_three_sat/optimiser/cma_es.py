"""
CMA-ES Optimizer Class

Author: Vivek Katial
"""

import numpy as np
import cma


class CMA_ES:
    """This class is an Object for the CMA-ES Optimisation algorithm

    Attributes
    ----------
        vars : list
            A list of variables that need to be optimised (e.g. alpha_i and beta_i)
        cost_function : func
            A cost function with ``callback()`` that we're evaluating

    Example
    --------
    >>> from qaoa_three_sat.optimiser.nelder_mead import NelderMead
    >>> CMA_ES(vars_vec = [0,0], cost_function=rosen)
    >>> CMA_ES.optimise()
    """

    def __init__(self, vars_vec, cost_function, options):
        """
        Initialisation method on the class for rotations
        """
        self.vars_vec = vars_vec
        self.cost_function = cost_function
        self.options = options

    def optimise(self):
        """Optimisation Method for CMA-ES"""

        std = np.std(self.vars_vec)
        vars_vec = self.vars_vec

        es = cma.CMAEvolutionStrategy(vars_vec, std)
        es.optimize(self.cost_function)
