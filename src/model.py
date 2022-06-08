import numpy as np
from mesa.model import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import Voter
import random




def mean_opinion(model):
    """Return the mean opinion of the agents in the given `model`
    """
    agent_opinion = [agent.opinion for agent in model.schedule.agents]
    active=agent_opinion.count(2)
    passive=agent_opinion.count(3)
    cops=agent_opinion.count(4)
    return [active,passive,cops]
    


class VoterModel(Model):
    """TODO"""
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
                    opinion=3 
                else:
                    opinion=1
                agent = Voter(
                    (x, y), 
                    self, 
                    opinion, 
                    risk_aversion=np.random.uniform(low=0.0, high=1.0),
                    grievance=np.random.uniform(low=0.0, high=1.0), 
                    jail_time=2
                )
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
        


        self.datacollector = DataCollector(
            model_reporters={"MeanOpinion": mean_opinion},  # A function to call
            agent_reporters={"Opinion": "opinion"})  # An agent attribute

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)

        #self.grid.move_to_empty()
        self.schedule.step()

        if self.schedule.steps > self.max_steps:
            self.running = False
