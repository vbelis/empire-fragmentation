# Model Class definition. The model attributes are defined, the agent are placed
# on the grid with their attribues set.

import numpy as np
from mesa.model import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import Native
import random


def agent_states(model):
    """
    Return the number of rebels (active citizens), pro-empire (quiet/passive
    citizens), prisoners, and propagandists (cops) at a given time step. As
    a starting point of the project, the propagandists are kept constant
    throughout the simulation.
    """
    agent_state = [agent.state for agent in model.schedule.agents]
    active = agent_state.count(2)
    passive = agent_state.count(3)
    prisoners = agent_state.count(4)
    cops = agent_state.count(1)
    return [active, passive, prisoners, cops]

# FIXME more elegant and computationally inexpensive...
def get_rebels(model):
    return agent_states(model)[0]

def get_passive(model):
    return agent_states(model)[1]

def get_prisoners(model):
    return agent_states(model)[2]

def get_cops(model):
    return agent_states(model)[3]

def percieved_gl(model):
    agent_state = [agent.government_legitimacy for agent in model.schedule.agents]
    return np.mean(agent_state)

def grievance(model):
    agent_state = [agent.grievance for agent in model.schedule.agents]
    return np.mean(agent_state)


class EmpireModel(Model):
    """
    Mesa agent-based  model describing the evolution of an empire in which 
    rebellions movements occur. The simulations takes place on a 2d grid.
    For a detailed description of the model, take in `docs/`.
    """

    def __init__(
        self,
        width: int,
        height: int,
        percentage_of_cops: float,
        percent_of_citizens: float,
        jail_time: int,
        max_steps: int,
        government_legitimacy: float,
        decrease_legit: bool,
        jail_time_random:bool = False,
    ):
        """
        Args:
            width: The width of the square grid.
            height: Height of the square grid.
            percentage_of_cops: The initial percentage of cops/propagandists on
                                the grid. Stays constant through time.
            percent_of_citizens: The initial percentage of citizen agents on the 
                                 grid. 
            jail_time: The number of time-steps that a citizen will stay in jail
                       if imprisoned by a cop.
            max_steps: Maximum steps of the simulation.
            government_legitimacy: The perceived legitimace/popularity of the 
                                   empire by its citizens.
            decrease_legit: A flag that dictates whether the `government_legitimacy`
                            will descrease at every time-step.
            jail_time_random: A flag that dicstates whether the jail assignment is
                              stochastic.
        """
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.max_steps = max_steps
        self.grid = SingleGrid(width=width, height=height, torus=True)

        for (_, x, y) in self.grid.coord_iter():
            if random.random() < percentage_of_cops + percent_of_citizens:
                if random.random() < percent_of_citizens:
                    state = 3
                else:
                    state = 1
                agent = Native(
                    (x, y),
                    self,
                    state,
                    risk_aversion=np.random.uniform(low=0.0, high=1.0),
                    perceived_hardship=np.random.uniform(low=0.0, high=1.0),
                    government_legitimacy=government_legitimacy,
                    threshold=np.random.normal(loc=0.1,scale=0.1),
                    decrease_legit=decrease_legit,
                    jail_time=random.randrange(jail_time)
                    if jail_time_random
                    else jail_time,
                )
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

        self.datacollector = DataCollector(
            model_reporters={
                "Rebels": get_rebels,
                "Pro-empire": get_passive,
                "Prisoners": get_prisoners,
                "Propagandists": get_cops,
                "Government Legitemicy": percieved_gl,
                "Grievance": grievance,
            }
        )

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()

        if self.schedule.steps > self.max_steps:
            self.running = False
