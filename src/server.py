# Module used to visualise the simulation on a 2-d grid in an interactive manner.

import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import ChartModule 
from mesa.visualization.UserParam import UserSettableParameter 
from model import VoterModel

# Set the model parameters
params = {"width": 50, 
          "height": 50,
          "percentage_of_cops":0.3,
          "percent_of_citizens":0.6
         }


def portrayTwoDimCell(agent):
    assert agent is not None
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": agent.x,
        "y": agent.y,
        "Color": "black" if agent.opinion == 1 else #cops 
                 "red" if agent.opinion == 2 else "blue" #rebels and pro-empire
    }


width = params['width']
height = params['height']
pixel_ratio = 10
grid = CanvasGrid(portrayTwoDimCell, width, height,
                  width*pixel_ratio, height*pixel_ratio)

chart = ChartModule([{"Label": "MeanOpinion",
                      "Color": "Blue"}],
                    data_collector_name='datacollector') # self.datacollector in VoterModel

server = ModularServer(VoterModel, [grid, chart],
                       "Voter Model", params)
