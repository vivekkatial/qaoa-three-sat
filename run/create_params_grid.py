"""A script to create the parameter search space for QAOA

Author: Vivek Katial
"""

from os import path
from itertools import product
import yaml
import json
import logging

def load_yaml_file(filename):
    """ Load parameter YAML file

    :param filename: A filename for parameter file
    :type filename: str
    :returns: A dictionary containing the parameter fiel
    :rtype: {dict}
    """
    param_file = path.join("params", filename)
    with open(param_file) as file:
        params = yaml.load(file, Loader=yaml.FullLoader)
    return params

def create_nelder_mead_opts(budget):
    """A function to create nelder-mead options dictionary
    
    :param budget: Budget given to Nelder-mead
    :type budget: int
    :returns: A string representing a dictionary
    :rtype: {str}
    """
    
    optimisation_opts = "{'classical_opt_alg':'nelder-mead', 'xtol': 0.001, 'disp' : True, 'adaptive' : True, 'budget':%s}"%(budget)

    return optimisation_opts

def create_cma_es_opts(budget):
    """A function to create CMA-ES options dictionary
    
    :param budget: Budget given to CMA-ES
    :type budget: int
    :returns: A string representing a dictionary
    :rtype: {str}
    """
    
    optimisation_opts = "{'classical_opt_alg':'cma-es', 'budget':%s}"%(budget)
    
    return optimisation_opts

def create_optimisation_dict(classical_opt_alg, budget):
    """ Build optimisation dict based on algorithm selected
    
    :param classical_opt_alg: Classical alg
    :type classical_opt_alg: str
    :param budget: Budget given for function evals
    :type budget: int
    :returns: text for jSON dict
    :rtype: {str}
    :raises: ValueError
    """
    if classical_opt_alg not in ["nelder-mead", "cma-es"]:
        raise ValueError("classical_opt_alg currently not implemented")
    if classical_opt_alg == "nelder-mead":
        optimisation_opts = create_nelder_mead_opts(budget)
    elif classical_opt_alg == "cma-es":
        optimisation_opts = create_cma_es_opts(budget)
    return optimisation_opts


def main():

    params_grid = load_yaml_file("params_grid.yml")
    params_template = load_yaml_file("params_template.yml")

    logging.basicConfig(level=logging.INFO)


    
    l_classical_opt_alg = params_grid["classical_opt_alg"]
    l_budget = params_grid["budget"]
    l_n_rounds = params_grid["n_rounds"]

    for inst in product(l_classical_opt_alg, l_budget, l_n_rounds):

        instance = params_template
        instance["classical_optimisation"]["classical_opt_alg"] = inst[0]
        instance["classical_optimisation"]["optimisation_opts"] = create_optimisation_dict(inst[0], inst[1])
        instance["classical_optimisation"]["n_rounds"] = inst[2]
        instance["classical_optimisation"]["alpha_trial"] = str([0] * int(inst[2]))
        instance["classical_optimisation"]["beta_trial"] = str([0] * int(inst[2]))
        
        classical_instance_file = '_'.join(str(i) for i in inst) + ".json"
        outpath = path.join("params", "ready", classical_instance_file)
        logging.info("Writing \t" + outpath)
        
        with open(outpath, 'w') as outfile:
            json.dump(instance, outfile, indent=4)
    
    

if __name__ == '__main__':
    main()