"""
Nelder-Mead Optimizer Class

Author: Vivek Katial
"""

import numpy as np
from scipy.optimize import minimize


class NelderMead:
    """An optimisation object class

    Attributes:
        vars (:float:`list`): A list of variables that need to be optimised (e.g. \alpha_i and \beta_i)
        cost_function (:callback:`func`): A cost function with `callback()` that we're evaluating
        options (:obj:`dict`): Optimisation Algorithm Parameters Dictionary

    """

    def __init__(self, vars_vec, cost_function, options):
        """
        Initialisation method on the class for rotations

        Args:
            vars (:float:`list`): A list of variables that need to be optimised (e.g. \alpha_i and \beta_i)
            cost_function (:callback:`func`) A cost function with `callback()` that we're evaluating

        """
        self.vars_vec = vars_vec
        self.cost_function = cost_function
        self.options = options

    def optimise(self):
        """
        Method to optimise the circuit
        """

        # Build a simplex (add epsilon to alpha / add epsilon to beta)
        vars_vec_0 = self.vars_vec
        # vars_vec_1 = [i + self.options["simplex_area_param"] for i in vars_vec_0]
        # vars_vec_2 = [i - self.options["simplex_area_param"] for i in vars_vec_0]

        # Build the simplex triangle for the algorithm
        # simplex = np.array([vars_vec_0, vars_vec_1, vars_vec_2], dtype=object)

        # Optimise alpha and beta using the cost function <s|H|s>
        res = minimize(
            self.cost_function,
            x0=vars_vec_0,
            method="nelder-mead",
            options={
                "xtol": self.options["xtol"],
                "disp": self.options["disp"],
                # "initial_simplex": simplex,
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
