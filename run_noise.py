from src.noiseagent import Agent
import numpy as np
import pandas as pd
from utils import arg_parser


def run(args):
    # Setup agents
    agents = [Agent(args.c) for _ in range(args.N)]

    # Record results
    entrance_rates = []

    # History of profitability
    history = []

    # Run for T time steps
    for t in range(args.T):
        entrance_rate = sum(agent.action == "enter" for agent in agents) / len(agents)
        entrance_rates.append(entrance_rate)

        # If the agent should have entered or not at t
        profitable = entrance_rate <= args.c

        # Treat as a float for averaging over
        history.append(float(profitable))

        # Progress each agent
        for agent in agents:
            # Agents only see most recent M of history
            agent.tick(args.c, history[-args.M:])

    # Prepare outcomes
    decisions = []

    #for agent in agents:
        #decisions.append(agent.decision_history)

    entrance_rates = entrance_rates

    # Return outcomes for plotting
    return {
        "entrance_rates": np.asarray(entrance_rates),
        #"decisions": np.asarray(decisions),
    }


def main(args):
    entrance_rates = []
    agent_decisions = []

    # Run multiples times to account for stochasticity
    n_runs = 30
    for _ in range(n_runs):
        individual_run = run(args)

        entrance_rates.append(individual_run["entrance_rates"])
        #agent_decisions.append(individual_run["decisions"])

    # To data frames for easier file processing
    #agent_decisions = pd.DataFrame(np.concatenate(agent_decisions))
    entrance_rates = pd.DataFrame(np.asarray(entrance_rates).T)

    filename = f"{args.c}-{args.lr}-{args.N}"

    output_folder = args.output_folder
    #agent_decisions.to_csv(output_folder + "decisions-" + filename + ".csv")
    entrance_rates.to_csv(output_folder + "attendance-" + filename + ".csv")


if __name__ == '__main__':
    args = arg_parser()
    main(args)

