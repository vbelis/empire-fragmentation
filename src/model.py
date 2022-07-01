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


def griviance(model):
    agent_state = [agent.grievance for agent in model.schedule.agents]
    return np.mean(agent_state)


class EmpireModel(Model):
    """
    TODO
    """

    def __init__(
        self,
        width,
        height,
        percentage_of_cops,
        percent_of_citizens,
        jail_time,
        max_steps,
        government_legitimacy,
        decrease_legit,
        jail_time_random=False,
    ):
        """
        Args: TODO
        """
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.max_steps = max_steps
        self.grid = SingleGrid(width=width, height=height, torus=True)
        # self.running = True

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
                    # threshold=np.random.normal(),
                    government_legitimacy=government_legitimacy,
                    threshold=0.1,  # np.random.uniform(low=0.0, high=1.0),
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
                "Griviance": griviance,
            }
        )  # Need to be Callables
        # agent_reporters={"state": "state"})  # An agent attribute

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        # self.grid.move_to_empty()
        self.schedule.step()

        if self.schedule.steps > self.max_steps:
            self.running = False
