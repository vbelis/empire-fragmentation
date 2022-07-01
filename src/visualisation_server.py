# Module used to visualise the simulation on a 2-d grid in an interactive manner.

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import EmpireModel

frac_cops = UserSettableParameter(
    "slider", "Fraction of cops", value=0.04, min_value=0.05, max_value=0.9, step=0.05
)
frac_citizens = UserSettableParameter(
    "slider", "Fraction of citizens", value=0.7, min_value=0.1, max_value=0.9, step=0.05
)
jail_time = UserSettableParameter(
    "slider", "Jail time", value=5, min_value=1, max_value=20, step=1
)
government_legitimacy = UserSettableParameter(
    "slider",
    "Empire popularity",
    value=0.84,
    min_value=0.0,
    max_value=1.0,
    step=0.05,
)
jail_time_random = UserSettableParameter("checkbox", "Random jail time", value=False)
decrease_legit = UserSettableParameter(
    "checkbox", "Decrease empire legitimacy", value=False
)

max_steps = UserSettableParameter("number", "Time step", value=100)
# Set the model parameters
params = {
    "width": 50,
    "height": 50,
    "percentage_of_cops": frac_cops,
    "percent_of_citizens": frac_citizens,
    "jail_time": jail_time,
    "jail_time_random": jail_time_random,
    "max_steps": max_steps,
    "government_legitimacy": government_legitimacy,
    "decrease_legit": decrease_legit,
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
    if agent.state == 1:
        portrayal["Color"] = "black"  # cops
    elif agent.state == 2:
        portrayal["Color"] = "red"  # rebels
    elif agent.state == 3:
        portrayal["Color"] = "blue"  # pro-empire
    else:
        portrayal["Color"] = "white"  # prisoner or empty slot.
    return portrayal


width = params["width"]
height = params["height"]
pixel_ratio = 10
grid = CanvasGrid(
    portrayTwoDimCell, width, height, width * pixel_ratio, height * pixel_ratio
)
chart1 = ChartModule(
    [
        {"Label": "Rebels", "Color": "Red"},
        {"Label": "Pro-empire", "Color": "Blue"},
        {"Label": "Prisoners", "Color": "Green"},
        {"Label": "Propagandists", "Color": "Black"},
    ],
    data_collector_name="datacollector",
)  # self.datacollector in EmpireModel
chart2 = ChartModule(
    [
        {"Label": "Government Legitemicy", "Color": "Red"},
        {"Label": "Griviance", "Color": "Blue"},
    ],
    data_collector_name="datacollector",
)  # self.datacollector in EmpireModel

server = ModularServer(
    EmpireModel, [grid, chart1, chart2], "Empire Fragmentation", params
)

if __name__ == "__main__":

    server.launch()
