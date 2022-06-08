import numpy as np
from mesa.agent import Agent
import random
import math
#k=2.3

class Voter(Agent):
    def __init__(self, unique_id, model, opinion, risk_aversion, grievance, 
                 jail_time, threshold=0.1, time_in_jail=0):
        """ TODO
        Args:
            TODO
        """

        super().__init__(unique_id=unique_id, model=model)
        self.x, self.y = unique_id
        self.opinion = opinion
        self._next_opinion = None
        self.threshold = threshold
        self.risk_aversion=risk_aversion
        self.grievance=grievance
        self.time_in_jail=time_in_jail
        self._next_time_in_jail = 0
        self.jail_time=jail_time

    @property
    def neighbors_cells(self):
        return self.model.grid.get_neighborhood(pos=(self.x, self.y), moore=True)
    
    @property
    def neighbors(self):
        return self.model.grid.get_neighbors(pos=(self.x, self.y), moore=True)

    @property
    def net_risk(self):
        #num_ones = self.opinion
        #cops->1
        #active->2
        #pasive->3
        #prison->4
        cops=0
        active=0
        passive=0
        for neighbor in self.neighbors:
            if neighbor==1:
                cops+= 1 #neighbor.opinion
            elif neighbor==2:
                active+=1
            elif neighbor==3:
                passive+=1
        #ESTIMATED-ARREST-PROBABILITY (eap)
        if active!=0:
            eap = 1-math.exp(-2.3*np.math.floor(cops/active))#num_ones / 5 if include_self else num_ones / 4
        #NET-RISK (nr)
            nr=eap*self.risk_aversion#frequency_zero = 1 - frequency_one
        else:
            nr=0

        return nr

    #@property
    #def indicator_z(self):
    #    if self.model.strategy == "majority":
    #        z = self.local_frequency[1] - self.threshold
    #    else:
    #        z = self.threshold - self.local_frequency[1]
    #    return z


################################################################################
######################   YOUR INPUT NEEDED BELOW  ##############################

    def epstein(self):
        """Compute and set the `self._next_opinion` 
        according to the linear voter model
        """
        #neighbors_values= [neighbor.opinion for neighbor in self.neighbors]
        if self.opinion==2 or 3:
            if self.grievance-self.net_risk>self.threshold:
                self._next_opinion=2
            else:
                self._next_opinion=3
        if self.opinion==4:
            if self.time_in_jail<self.jail_time-1:
                self._next_time_in_jail=self.time_in_jail+1
                self._next_opinion=4
            else:
                self._next_opinion=3
                self._next_time_in_jail=0
                self.model.grid.place_agent(self,self.model.grid.find_empty())

        if self.opinion==1:
            self._next_opinion=1
            prospect_prisoners=list()
            for n in self.neighbors_cells:
                x,y=n
                if self.model.grid[x][y]!= None and self.model.grid[x][y].opinion==2:
                    prospect_prisoners.append(n)
            if not prospect_prisoners:
                pass
            else:
                prisoner=random.choice(prospect_prisoners)
                x, y = prisoner
                self.model.grid[x][y]._next_opinion=4
                self.model.grid[x][y] = None
                self.model.grid.empties.add(prisoner)
                
                

            #if 2 in self.neighbors:
                #self._next_opinion=1

            


        #self._next_opinion=random.choice(neighbors_values)

    # def deterministic(self):
    #     """Compute and set the `self._next_opinion` 
    #     according to the deterministic voter model
    #     """
    #     if self.model.strategy == "majority" and self.indicator_z>0:
    #         self._next_opinion=1
    #     elif self.model.strategy == "majority" and self.indicator_z<0:
    #         self._next_opinion=self.opinion*0


        
    #     if self.model.strategy == "minority" and self.indicator_z<0:
    #         self._next_opinion=0
    #     elif self.model.strategy == "minority" and self.indicator_z>0:
    #         self._next_opinion=1
################################################################################
################################################################################


    def step(self):
        #self._next_opinion = self.opinion
        self.model.grid.move_to_empty(self)
        #if self.model.model_type == "linear":
        self.epstein()
        #else:
        #    self.deterministic()

    def advance(self):
        self.opinion = self._next_opinion
        self.time_in_jail=self._next_time_in_jail
       
