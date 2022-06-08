# Module used to visualise the simulation on a 2-d grid in an interactive manner.

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import ChartModule 
from mesa.visualization.UserParam import UserSettableParameter 
from model import EmpireModel

# Set the model parameters
params = {"width": 50, 
          "height": 50,
          "percentage_of_cops":0.3,
          "percent_of_citizens":0.6
         }

"""
fr_one_slider = UserSettableParameter('slider', 'Fraction of agents with state=1', 
                                        value=.5, min_value=0.1, max_value=.9, step=0.1)
model_type_option = UserSettableParameter('choice', 'Type', value='linear',
                                              choices=['linear', 'deterministic'])
strategy_option = UserSettableParameter('choice', 'Strategy', value='majority',
                                              choices=['majority', 'minority'])
"""

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
        "Color": "black" if agent.state == 1 else #cops 
                 "red" if agent.state == 2 else "blue" #rebels and pro-empire
    }


width = params['width']
height = params['height']
pixel_ratio = 10
grid = CanvasGrid(portrayTwoDimCell, width, height,
                  width*pixel_ratio, height*pixel_ratio)

chart = ChartModule([{"Label": "Meanstate",
                      "Color": "Blue"}],
                    data_collector_name='datacollector') # self.datacollector in EmpireModel

server = ModularServer(EmpireModel, [grid, chart],
                       "Empire Fragmentation", params)

if __name__ == "__main__":
    server.launch()
