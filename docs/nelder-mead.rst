Nelder-Mead
============

The Nelder-Mead Simplex algorithm, devised by J.A. Nelder and
R. Mead [1]_, is a direct search method of optimization for
finding local minimum of an objective function of several
variables. The implementation of Nelder-Mead Simplex algorithm is
a variation of the algorithm outlined in [2]_ and [3]_. As noted,
terminating the simplex is not a simple task:

"For any non-derivative method, the issue of termination is
problematical as well as highly sensitive to problem scaling.
Since gradient information is unavailable, it is provably
impossible to verify closeness to optimality simply by sampling f
at a finite number of points.  Most implementations of direct
search methods terminate based on two criteria intended to reflect
the progress of the algorithm: either the function values at the
vertices are close, or the simplex has become very small."

"Either form of termination-close function values or a small
simplex-can be misleading for badly scaled functions."

References
----------

.. [1] "A simplex method for function minimization", J.A. Nelder
           and R. Mead (Computer Journal, 1965, vol 7, pp 308-313)
           https://doi.org/10.1093%2Fcomjnl%2F7.4.308

.. [2] "Convergence Properties of the Nelder-Mead Simplex
        Algorithm in Low Dimensions", Jeffrey C. Lagarias, James
        A. Reeds, Margaret H. Wright, Paul E. Wright , SIAM Journal
        on Optimization, Vol. 9, No. 1 (1998), pages 112-147.
        http://citeseer.ist.psu.edu/3996.html

.. [3] "Direct Search Methods: Once Scorned, Now Respectable"
           Wright, M. H. (1996) in Numerical Analysis 1995
           (Proceedings of the 1995 Dundee Biennial Conference in
           Numerical Analysis, D.F. Griffiths and G.A. Watson, eds.),
           191-208, Addison Wesley Longman, Harlow, United Kingdom.
           http://citeseer.ist.psu.edu/155516.html