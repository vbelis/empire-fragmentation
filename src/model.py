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
    


class EmpireModel(Model):
    """
    TODO
    """
    def __init__(self, width, height,percentage_of_cops,percent_of_citizens, max_steps=30):
        """
        Args: TODO
        """
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.max_steps = max_steps
        self.grid = SingleGrid(width=width, height=height, torus=True)

        for (_, x, y) in self.grid.coord_iter():
            if random.random() < percentage_of_cops+percent_of_citizens:
                if random.random() < percent_of_citizens:
                    state=3 
                else:
                    state=1
                agent = Native(
                    (x, y), 
                    self, 
                    state, 
                    risk_aversion=np.random.uniform(low=0.0, high=1.0),
                    grievance=np.random.uniform(low=0.0, high=1.0), 
                    jail_time=2
                )
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
        


        self.datacollector = DataCollector(
            model_reporters={"AgentStates": agent_states},  # A function to call
            agent_reporters={"state": "state"})  # An agent attribute

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)

        #self.grid.move_to_empty()
        self.schedule.step()

        if self.schedule.steps > self.max_steps:
            self.running = False
