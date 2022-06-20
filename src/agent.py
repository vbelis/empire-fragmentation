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
    def __init__(self, unique_id, model, state, risk_aversion, perceived_hardship, 
                 jail_time, government_legitimacy, decrease_legit, threshold=0.1,
                 time_in_jail=0):
        """ TODO
        Args:
            TODO
        """
        super().__init__(unique_id=unique_id, model=model)
        self.x, self.y = unique_id
        self.state = state
        self._next_state = None
        self._next_gl = None
        self._next_grievance=None
        self.threshold = threshold
        self.risk_aversion=risk_aversion
        self.time_in_jail=time_in_jail
        self._next_time_in_jail = 0
        self.jail_time=jail_time
        self.perceived_hardship = perceived_hardship
        
        # The agents have the same opinion about the government but maybe we
        # can make it subjective with mean=self.government_legitimacy.
        self.government_legitimacy= government_legitimacy
        # We can adjust the law with which legitimacy decreases:
        self.decrease_legit = decrease_legit
        self.legit_step = self.government_legitimacy/model.max_steps # L->0 always
        self.grievance=self.perceived_hardship*(1-self.government_legitimacy)
        
        # @paper: Unifrom distribution for perceived_hardship.
    
    def evolve_government_legitimacy(self):
        """
        Evolves (typically decreases) the government_legitimacy at every time
        step. Can be extended to support different ways of evolution. E.g.,
        linear, exponential, or even evolutions that don't necessarily decrease
        the legitimacy of the empire.
        """
        self._next_gl = self.government_legitimacy/1.2 #- self.legit_step
        
        if self.government_legitimacy <= 0.: return 0
        else: return self._next_gl
    @property 
    def Griviance(self):
        return self.perceived_hardship*(1-self.government_legitimacy)
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
    def change_in_grivience(self):
        if self.decrease_legit:
            self.grievance=self.perceived_hardship*(1-self.government_legitimacy)

    def decision_rule(self):
        """Compute and set the `self._next_state` 
        according to the linear Native model
        """
        #neighbors_values= [neighbor.state for neighbor in self.neighbors]
        if self.state==2 or 3:
            if self.Griviance-self.net_risk>self.threshold:
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
        # FIXME Should we put this check here or in self.advance?
        if self.decrease_legit: 
            self._next_gl=self.evolve_government_legitimacy()
            self._next_grievance = self.perceived_hardship*(1-self.government_legitimacy)
        else:
            self._next_gl=self.government_legitimacy
            self._next_grievance=self.grievance

        self.model.grid.move_to_empty(self)
        self.decision_rule()

    def advance(self):
        self.state = self._next_state
        self.grievance=self._next_grievance
        self.government_legitimacy=self._next_gl
        self.time_in_jail=self._next_time_in_jail
       

