
import matplotlib.pyplot as plt
import numpy as np
from random import sample
from model import EmpireModel
from mesa.batchrunner import batch_run
from mesa.batchrunner import FixedBatchRunner
if __name__ ==  '__main__':
    param_set = dict(height=50, # Height and width are constant
                 width=50,
                 jail_time= 10,
                 
                 decrease_legit =False,
                 jail_time_random=False,
                 # Vary density from 0.01 to 1, in 0.01 increments:
                 percentage_of_cops=0.1,#np.linspace(0,0.1,3)[1:],
                 percent_of_citizens=np.linspace(0,0.7,21)[1:],
                 government_legitimacy=0.85,
                 max_steps=100)#np.linspace(0,1,101)[1:])

    param_run = batch_run(EmpireModel, param_set,iterations= 1,data_collection_period=-1)#, max_steps=1) #batch_run


    print(len(param_run))
    print(param_run)
    #print(param_run[len(param_run)-1]['AgentID'])
    #print(param_run[1:10])