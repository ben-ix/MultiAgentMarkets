from src.agent import Agent
import numpy as np


class Market:
    agents = None
    entrance_rates = None
    history = None
    N = None
    c = None
    M = None

    def __init__(self, N, c=0.6, lr=1, M=10):
        self.N = N
        self.c = c
        self.M = M

        _cache = {}  # Shared cache between all agents to avoid recomputing decisions
        self.agents = [Agent(c, lr, cache=_cache) for _ in range(N)]

        # Record results
        self.entrance_rates = []

        # History of profitability
        self.history = []

    def run(self, T):
        """
        Run the market for T time steps (ticks).
        """
        # Run for T time steps
        for t in range(T):
            self.tick()

    def tick(self):
        """
        Progress the market one time step
        """
        entrance_rate = sum(agent.action == "enter" for agent in self.agents) / len(self.agents)
        self.entrance_rates.append(entrance_rate)

        # If the agent should have entered or not at t
        profitable = entrance_rate <= self.c

        # Treat as a float for averaging over
        self.history.append(float(profitable))

        # Progress each agent
        for agent in self.agents:
            # Agents only see most recent M of history
            agent.tick(self.c, self.history[-self.M:])

    def results(self):
        """
        Return a dictionary of the values to track, includes:
            - entrance_rates: The proportion of agents who attended at each time step (T)
            - decisions: A 2d array which has each agents decision history (NxT)
            - resources: A 2d array which has each agents resource history (NxT)
        """

        if not self.entrance_rates:
            raise Exception("Must call run() or tick() first")

        # Prepare outcomes
        decisions = [agent.decision_history for agent in self.agents]
        resources = [agent.resource_history for agent in self.agents]

        return {
            "entrance_rates": np.asarray(self.entrance_rates),
            "decisions": np.asarray(decisions),
            "resources": np.asarray(resources),
        }

