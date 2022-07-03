# Script for running simulations in parallel, scanning different parameter
# values. The values that the batrch_runner will scan can be tweaked in the
# dictionary bellow. The output is saved in a pandas dataframe pickle file.

import argparse
import numpy as np
from model import EmpireModel
from mesa.batchrunner import batch_run
import pandas as pd


def main():
    """
    Defines and runs model simulations in parallel, scanning the parameter space
    defined by the `parameter_set` dictionary. Concatenates the outputs of the 
    simulations in a single pandas dataframe and saves it into a .pkl file.
    """

    out_path = get_arguments()
    param_set = dict(
        height=50,  # Height and width are constant
        width=50,
        jail_time=[10, 15, 20],
        decrease_legit=True,
        jail_time_random=False,
        percentage_of_cops=np.linspace(0, 0.25, 50)[1:],
        percent_of_citizens=np.linspace(0, 0.7, 50)[1:],
        government_legitimacy=0.85,
        max_steps=100,
    )
    param_run = batch_run(
        EmpireModel, param_set, iterations=5, data_collection_period=-1
    )
    print("Saving the dataframe to pickle file...")
    df = pd.DataFrame(param_run)
    df.to_pickle(out_path)

def get_arguments() -> str:
    """
    Parses command line arguments. In this case is simply one argument, the path
    to the output file of the script.
    
    Returns: The output path of the dataframe produced in the simulation.
    """
    parser = argparse.ArgumentParser(formatter_class=
                                 argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
    "--out",
    type=str,
    required=True,
    help="Path to save the simulation results produced by the batchrunner in "
          "dataframe format (.pkl file). Include the .pkl suffix.",
    )
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    main()
