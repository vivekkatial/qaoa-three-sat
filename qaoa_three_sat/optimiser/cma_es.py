"""
CMA-ES Optimizer Class

Author: Vivek Katial
"""

import numpy as np
import cma
import random
from math import pi


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

    Details
    -------
    Return the list provided in `CMAEvolutionStrategy.result` appended
    with termination conditions, an `OOOptimizer` and a `BaseDataLogger`::
        res = es.result + (es.stop(), es, logger)

        where
        - ``res[0]`` (``xopt``) -- best evaluated solution
        - ``res[1]`` (``fopt``) -- respective function value
        - ``res[2]`` (``evalsopt``) -- respective number of function evaluations
        - ``res[3]`` (``evals``) -- number of overall conducted objective function evaluations
        - ``res[4]`` (``iterations``) -- number of overall conducted iterations
        - ``res[5]`` (``xmean``) -- mean of the final sample distribution
        - ``res[6]`` (``stds``) -- effective stds of the final sample distribution
        - ``res[-3]`` (``stop``) -- termination condition(s) in a dictionary
        - ``res[-2]`` (``cmaes``) -- class `CMAEvolutionStrategy` instance
        - ``res[-1]`` (``logger``) -- class `CMADataLogger` instance
    """

    def __init__(self, vars_vec, cost_function, options):
        """
        Initialisation method on the class for rotations
        """
        self.vars_vec = vars_vec
        self.cost_function = cost_function
        self.options = options
        self.budget = options["budget"]
        self.iterations = 1

    def optimise(self):
        """Optimisation Method for CMA-ES"""

        std = np.std(self.vars_vec)
        vars_vec = self.vars_vec
        vars_vec_0 = [random.uniform(-pi, pi) for i in range(len(self.vars_vec))]

        # Results from CMA-ES process
        res = cma.fmin(
            self.cost_function, vars_vec_0, std, options={"maxfevals": self.budget}
        )

        # Return the best function evaluation
        self.vars_vec = res[0]

        return 0
