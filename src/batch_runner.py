import matplotlib.pyplot as plt
import numpy as np
from random import sample
from model import EmpireModel
from mesa.batchrunner import batch_run
from mesa.batchrunner import FixedBatchRunner
import pandas as pd

if __name__ == "__main__":
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
    )  # , max_steps=1)
    print("Saving the dataframe to pickle file...")
    df = pd.DataFrame(param_run)
    df.to_pickle("./df_50_3_jailtime_Lto0.pkl")
