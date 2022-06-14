import random
from src.decisions import bounded_decision
from statistics import mean

utility = {
    "enter": 1,
    "overcrowded": -1,
    "stay out": 0
}


class Agent:
    c = None  # Enjoyable capacity
    lr = None  # Learning rate
    B = None  # Resources
    gamma = None  # Discount

    action = None  # Action is either enter or exit

    decision_confidence = None  # For tracking probability of action at each steo
    decision_history = None  # For tracking attendances at each step
    resource_history = None  # For tracking B rates at each step
    correct_history = None  # For tracking if correct/incorrect with choice at each step
    accumulated_payoff_history = None  # For tracking how the achieved payoff changes over time

    cache = None
    
    def __init__(self, c, max_lr, cache=None):
        self.c = c
        self.lr = random.uniform(0.01, max_lr)  # Each agent learns at different rates
        self.B = random.uniform(0, 10)  # And has different starting resources
        self.gamma = random.uniform(0, 0.95)  # To 0.95 so dont get 0.9999 and not decaying

        # Tracking/analytics
        self.decision_confidence = []
        self.decision_history = []
        self.resource_history = []
        self.correct_history = []
        self.accumulated_payoff_history = []

        self.cache = cache if cache is not None else {}
        
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

            # If the agent was incorrect, learn
            if not correct:
                self.learn()

            # Track correct rates
            self.correct_history.append(correct)

            # And accumulated payoffs
            last_payoff = self.accumulated_payoff_history[-1] if self.accumulated_payoff_history else 0
            self.accumulated_payoff_history.append(last_payoff + achieved_payoff)

        # [p(enter), p(exit)]
        base_outcome = mean(outcome_history) if outcome_history is not None else None  # Average over history
        probabilities = self.decision(base_outcome)

        # Choose stance based on likelihoods
        self.action = "enter" if random.random() <= probabilities[0] else "exit"

        # Tracking analytics for plotting
        self.decision_confidence.append(probabilities[0])  # Just need to track prob[0] as prob[1] is just 1-prob[0]
        self.decision_history.append(self.action == "enter")  # True or false for enter/exit
        self.resource_history.append(round(self.B, 2))  # Just stores to 2dp for plotting purposes

    def decision(self, base_outcome=None, k=0):
        resources = self.B * (self.gamma ** k)

        # Avoid recomputing in identical scenarios
        cache_key = (self.B, self.gamma, k, base_outcome)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Out of resources
        if resources < 0.0005:
            # Return prior

            # Indifferent to entering at beginning. Else prior is just enter based on if last time was profitable
            if base_outcome is None:
                prior = [1 * (self.c >= 0.5), 1 * (self.c < 0.5)]
            else:
                prior = [base_outcome, 1 - base_outcome]

            self.cache[cache_key] = prior

            return prior

        # Lower level thinkers
        try:
            lower_level = self.decision(base_outcome, k + 1)  # Recurse
        except RecursionError as e:
            print("Recursion error", self.B, self.gamma, k)
            raise e

        predicted_entrance = lower_level[0]  # Probability of entering

        # They enter if they think is uncrowded
        enter_payoff = utility["enter"] if predicted_entrance < self.c else utility["overcrowded"]

        # Fixed payoff for staying out
        stay_out_payoff = utility["stay out"]

        utilities = [enter_payoff, stay_out_payoff]

        outcome = bounded_decision(lower_level, resources, utilities)
        self.cache[cache_key] = outcome

        return outcome

    def learn(self):
        # learning just corresponds to increasing resources
        self.B += self.lr

    def correctness(self):
        # Have not competed yet
        if not self.correct_history:
            return 0

        return sum(self.correct_history) / len(self.correct_history)
