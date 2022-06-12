import numpy as np
from mesa.agent import Agent
import random
import math
#k=2.3

class Native(Agent):
    """
    Agents (called also 'natives' here) are devided into citizens and propagandists 
    (cops). The former can have two states: being a rebel (active), or pro-empire 
    (passive/quiet). The latter stay constant throughout. Both move randomly on the
    grid, obeying a Moore neighborhood (can change throughout the project) 
    and periodic boundary conditions. We have the following conventions about the agent
    states:
    - cops->1
    - active->2
    - pasive->3
    - prison->4
    """
    def __init__(self, unique_id, model, state, risk_aversion,perceived_hardship, 
                 jail_time, threshold=0.1, time_in_jail=0,government_legitimacy=0.84):
        """ TODO
        Args:
            TODO
        """
        super().__init__(unique_id=unique_id, model=model)
        self.x, self.y = unique_id
        self.state = state
        self._next_state = None
        self.threshold = threshold
        self.risk_aversion=risk_aversion
        self.time_in_jail=time_in_jail
        self._next_time_in_jail = 0
        self.jail_time=jail_time
        self.grievance=perceived_hardship*(1-government_legitimacy) # @paper: Unifrom distribution

    @property
    def neighbors_cells(self):
        return self.model.grid.get_neighborhood(pos=(self.x, self.y), moore=True)
    
    @property
    def neighbors(self):
        return self.model.grid.get_neighbors(pos=(self.x, self.y), moore=True)

    @property
    def net_risk(self):
        """
        Defines the 'net perceived risk' at every time step.
        """
        cops=0
        active=0
        passive=0
        for neighbor in self.neighbors:
            if neighbor==1:
                cops+= 1 #neighbor.state
            elif neighbor==2:
                active+=1
            elif neighbor==3:
                passive+=1
        #ESTIMATED-ARREST-PROBABILITY (eap)
        if active!=0:
            eap = 1-math.exp(-2.3*np.math.floor(cops/active))# here -2.3 is a tuninig parameter k (it can be another variable and nw is adopted from the paper)
        #NET-RISK (nr)
            nr=eap*self.risk_aversion # frequency_zero = 1 - frequency_one
        else:
            #eap = 1-math.exp(-2.3*np.math.floor(cops))
            #nr=eap*self.risk_aversion
            nr=0
        return nr

    def decision_rule(self):
        """Compute and set the `self._next_state` 
        according to the linear Native model
        """
        #neighbors_values= [neighbor.state for neighbor in self.neighbors]
        if self.state==2 or 3:
            if self.grievance-self.net_risk>self.threshold:
                self._next_state=2
            else:
                self._next_state=3
        if self.state==4:
            if self.time_in_jail<self.jail_time-1:
                self._next_time_in_jail=self.time_in_jail+1
                self._next_state=4
            else:
                self._next_state=3
                self._next_time_in_jail=0
                self.model.grid.place_agent(self,self.model.grid.find_empty())

        if self.state==1:
            self._next_state=1
            prospect_prisoners=list()
            for n in self.neighbors_cells:
                x,y=n
                if self.model.grid[x][y]!= None and self.model.grid[x][y].state==2:
                    prospect_prisoners.append(n)
            if not prospect_prisoners:
                pass
            else:
                prisoner=random.choice(prospect_prisoners)
                x, y = prisoner
                self.model.grid[x][y]._next_state=4
                self.model.grid[x][y] = None
                self.model.grid.empties.add(prisoner)
                
    def step(self):
        """
        Defines the simulation time step.
        """
        self.model.grid.move_to_empty(self)
        self.decision_rule()

    def advance(self):
        self.state = self._next_state
        self.time_in_jail=self._next_time_in_jail
       
