import random
from decisions import bounded_decision
from statistics import mean

utility = {
    "enter": 1,
    "overcrowded": -1,
    "stay out": 0
}


class Agent:
    """
    This is a random noise agent, who simply attends or doesnt randomly.
    There is no information processing or learning present.
    """
    c = None  # Enjoyable capacity

    action = None  # Action is either enter or exit

    decision_confidence = None  # For tracking probability of action at each steo
    decision_history = None  # For tracking attendances at each step
    correct_history = None  # For tracking if correct/incorrect with choice at each step
    accumulated_payoff_history = None  # For tracking how the achieved payoff changes over time

    cache = None
    
    def __init__(self, c):
        self.c = c

        # Tracking/analytics
        self.decision_confidence = []
        self.decision_history = []
        self.correct_history = []
        self.accumulated_payoff_history = []

        # Make decision on what to do
        self.tick(self.c)

    def tick(self, c, outcome_history=None):
        # For time dependant c's, update each tick
        self.c = c

        if outcome_history is not None:
            # The most recent timestep
            previous_outcome = outcome_history[-1]

            # If the agent was correct or not
            correct = (previous_outcome and self.action == "enter") or (not previous_outcome and self.action == "exit")

            # The achieved payoff depends on their choice and correctness
            if self.action == "exit":
                # Fixed payoff
                achieved_payoff = utility["stay out"]
            else:
                # Enter payoff depends if they were correct if they entered
                achieved_payoff = utility["enter"] if correct else utility["overcrowded"]

            # Track correct rates
            self.correct_history.append(correct)

            # And accumulated payoffs
            last_payoff = self.accumulated_payoff_history[-1] if self.accumulated_payoff_history else 0
            self.accumulated_payoff_history.append(last_payoff + achieved_payoff)

        # [p(enter), p(exit)]
        probabilities = self.decision()

        # Choose stance based on likelihoods
        self.action = "enter" if random.random() <= probabilities[0] else "exit"

        # Tracking analytics for plotting
        self.decision_confidence.append(probabilities[0])  # Just need to track prob[0] as prob[1] is just 1-prob[0]
        self.decision_history.append(self.action == "enter")  # True or false for enter/exit

    def decision(self):
        # Random decision
        random_prob = random.random()
        return [random_prob, 1-random_prob]