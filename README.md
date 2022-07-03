# Empire fragmentation

## Description
Investigating the phenomenon of empire fragmentation on a grid using agent based modelling. The goal of this project is to investigate the conditions under which an empire is overthrown due to a revolution. For more details, definitions, and the exact model description please check the report in `docs/empire_fragmentation_report.pdf`. 

## How to install
The easiest way play around with the simulations produced by the code is to install all dependencies within an anaconda environment, running on a linux device. After cloning the repository locally, you would need to run:
```
conda env create -f environment.yml
```
using the `environment.yml` file provided in the repo.

## Quick start
After installing and activating the conda environment you can start an interactive session of the simulation by running
```
python src/visualisation_server.py
```
You can play with the model parameters of interest, visualise the interaction of the agents on the grid, and extract insights from the corresponding plots.

|![this is the caption](https://github.com/vbelis/empire-fragmentation/blob/main/docs/simulation_visualisation.png?raw=true)
|:--:|
|The interactive simulation session.|

One can also configure the parameters and run many simulations in parallel using `src/batch_runner.py`. This script scans the defined parameter space and outputs ther final state of the simulation in `pandas` dataframe format. From this file we can get further insights about the model as it can be seen in the notebook `src/results_analysis.ipynb`.
