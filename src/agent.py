import numpy as np
from mesa.agent import Agent
from mesa.model import Model
import random
import math
# k=2.3


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

    For more information please check the report in `docs/`.
    """

    def __init__(
        self,
        unique_id: int,
        model: Model,
        state: int, # 0 or 1.
        risk_aversion: float,
        perceived_hardship: float,
        jail_time: int,
        government_legitimacy: float,
        decrease_legit: BlockingIOError,
        threshold: float = 0.1,
        time_in_jail:int =0,
    ):
        """
        Args:
            unique_id: The MESA id of the agent.
            model: The MESA model that we defined in `model.py`.
            state: The state of the agent; 0 if pro-empire 1 if a rebel.
            risk_aversion: The inherent risk aversion of the agent, defined in [0,1].
            perceived_hardship: Individual perceived hardship of the agent in [0,1].
            jail_time: Jail time that the agent stays in jail.
            government_legitimacy: The legitmacy of the government as viewed by the agent.
            decrease_legit: Flag the dictates whether the government will decrease in 
                            legitimacy at the next time step, according to the agent.
            threshold: Threshold that defines whether the agent will rebel or not.
            time_in_jail: Time the agent spent in jail.
        """
        super().__init__(unique_id=unique_id, model=model)
        self.x, self.y = unique_id
        self.state = state
        self._next_state = None
        self._next_gl = None
        self._next_grievance = None
        self.threshold = threshold
        self.risk_aversion = risk_aversion
        self.time_in_jail = time_in_jail
        self._next_time_in_jail = 0
        self.jail_time = jail_time
        self.perceived_hardship = perceived_hardship

        # The agents have the same opinion about the government but maybe we
        # can make it subjective with mean=self.government_legitimacy.
        self.government_legitimacy = government_legitimacy
        # We can adjust the law with which legitimacy decreases:
        self.decrease_legit = decrease_legit
        self.legit_step = self.government_legitimacy / model.max_steps  # L->0 always
        self.grievance = self.perceived_hardship * (1 - self.government_legitimacy)

        # @paper: Unifrom distribution for perceived_hardship.

    def evolve_government_legitimacy(self):
        """
        Evolves (typically decreases) the government_legitimacy at every time
        step. Can be extended to support different ways of evolution. E.g.,
        linear, exponential, or even evolutions that don't necessarily decrease
        the legitimacy of the empire.
        """
        self._next_gl = self.government_legitimacy / 1.2  # - self.legit_step

        if self.government_legitimacy <= 0.0:
            return 0
        else:
            return self._next_gl

    @property
    def neighbors_cells(self):
        """Get neighboring cells on the grid."""
        return self.model.grid.get_neighborhood(pos=(self.x, self.y), moore=True)

    @property
    def neighbors(self):
        """Get neighboring agents."""
        return self.model.grid.get_neighbors(pos=(self.x, self.y), moore=True)

    @property
    def net_risk(self) -> float:
        """
        Calculates and retuns 'net perceived risk' at every time step.
        """
        cops = 0
        active = 0
        passive = 0
        for neighbor in self.neighbors:
            if neighbor == 1:
                cops += 1  # neighbor.state
            elif neighbor == 2:
                active += 1
            elif neighbor == 3:
                passive += 1
        # ESTIMATED-ARREST-PROBABILITY (eap)
        if active != 0:
            eap = 1 - math.exp(
                -2.3 * np.math.floor(cops / active)
            )  # here -2.3 is a tuninig parameter k (it can be another variable and nw is adopted from the paper)
            # NET-RISK (nr)
            nr = eap * self.risk_aversion  # frequency_zero = 1 - frequency_one
        else:
            # eap = 1-math.exp(-2.3*np.math.floor(cops))
            # nr=eap*self.risk_aversion
            nr = 0
        return nr

    def decision_rule(self):
        """
        Compute and set the `self._next_state` according to the linear Native model
        """
        if self.state == 2 or 3:
            if self.grievance - self.net_risk > self.threshold:
                self._next_state = 2
            else:
                self._next_state = 3
        if self.state == 4:
            if self.time_in_jail < self.jail_time - 1:
                self._next_time_in_jail = self.time_in_jail + 1
                self._next_state = 4
            else:
                self._next_state = 3
                self._next_time_in_jail = 0
                self.model.grid.place_agent(self, self.model.grid.find_empty())

        if self.state == 1:
            self._next_state = 1
            prospect_prisoners = list()
            for n in self.neighbors_cells:
                x, y = n
                if self.model.grid[x][y] != None and self.model.grid[x][y].state == 2:
                    prospect_prisoners.append(n)
            if not prospect_prisoners:
                pass
            else:
                prisoner = random.choice(prospect_prisoners)
                x, y = prisoner
                self.model.grid[x][y]._next_state = 4
                self.model.grid[x][y] = None
                self.model.grid.empties.add(prisoner)

    def step(self):
        """Defines the simulation time step."""
        if self.decrease_legit:
            self._next_gl = self.evolve_government_legitimacy()
            self._next_grievance = self.perceived_hardship * (
                1 - self.government_legitimacy
            )
        else:
            self._next_gl = self.government_legitimacy
            self._next_grievance = self.grievance

        self.model.grid.move_to_empty(self)
        self.decision_rule()

    def advance(self):
        """Advance the agent by one time step."""
        self.state = self._next_state
        self.grievance = self._next_grievance
        self.government_legitimacy = self._next_gl
        self.time_in_jail = self._next_time_in_jail
