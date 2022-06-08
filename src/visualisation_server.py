# Module used to visualise the simulation on a 2-d grid in an interactive manner.

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule 
from mesa.visualization.UserParam import UserSettableParameter 

from model import EmpireModel

frac_cops = UserSettableParameter('slider', 'Fraction of cops', 
                                        value=.2, min_value=0.05, max_value=.9, step=0.05)
frac_citizens = UserSettableParameter('slider', 'Fraction of citizens', 
                                      value=.5, min_value=0.1, max_value=.9, step=0.05)
jail_time = UserSettableParameter('slider', 'Jail time', 
                                      value=2, min_value=1, max_value=5, step=1)

# Set the model parameters
params = {"width": 50, 
          "height": 50,
          "percentage_of_cops": frac_cops,
          "percent_of_citizens": frac_citizens,
          "jail_time": jail_time,
         }

def portrayTwoDimCell(agent):
    assert agent is not None
    portrayal = {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": agent.x,
        "y": agent.y,
    }        
    if agent.state == 1: portrayal["Color"] = "black" # cops
    elif agent.state == 2: portrayal["Color"] = "red" # rebels
    elif agent.state == 3: portrayal["Color"] = "blue" # pro-empire
    else: portrayal["Color"] = 'white' # prisoner or empty slot.
    return portrayal

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
