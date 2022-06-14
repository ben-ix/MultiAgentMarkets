import numpy as np
import pandas as pd
from utils import arg_parser
import pyNetLogo
import sys


def run(args, netlogo, random_seed=0):
    # Reproducibility
    netlogo.command(f"random-seed {random_seed}")

    # Set the global parameters
    netlogo.command(f"set T {args.T}")
    netlogo.command(f"set N {args.N}")
    netlogo.command(f"set memory-size {args.M}")
    netlogo.command(f"set overcrowding-threshold {args.c}")
    netlogo.command("setup")

    # Run for ticks. Exclude t0, as this is before any simulation run.
    outputs = netlogo.repeat_report(['attendance-rate'], reps=args.T, include_t0=False)

    # Save the attendance history of each agent
    decisions = netlogo.report('[attendance-history] of turtles')

    strategies = netlogo.report('[best-strategy-history] of turtles')

    return {
        "entrance_rates": outputs['attendance-rate'].values,
        "decisions": decisions,
        "strategies": strategies,
    }


def main(args):
    entrance_rates = []
    agent_decisions = []
    agent_strategies = []

    # Setup link to netlogo. We will reuse this across the various runs.
    # Note: when running on linux need to specify locations
    if sys.platform == 'darwin':
        # Can find automatically on mac
        netlogo = pyNetLogo.NetLogoLink()
    else:
        # Running on linux, so give specific location and version. Will need to change below
        # based on your netlogo configuration
        netlogo = pyNetLogo.NetLogoLink(netlogo_version="6.0", netlogo_home="/usr/local/netlogo/6.0.2/")

    # Load model
    netlogo.load_model('./src/comparison.nlogo')

    # Run multiples times to account for stochasticity
    n_runs = 30

    for i in range(n_runs):
        # Run netlogo code for given seed
        individual_run = run(args, netlogo, random_seed=i)
        entrance_rates.append(individual_run["entrance_rates"])
        agent_decisions.append(individual_run["decisions"])
        agent_strategies.append(individual_run["strategies"])

    # Clean up
    netlogo.kill_workspace()

    # Combine strategies into shape (runs * agents, timesteps, strategies)
    agent_strategies = np.concatenate(agent_strategies)

    # Join all the strategies together into shape (runs * agents, timesteps) where each timestep is the strategy string
    # we do this so we have a 2d array, not a 3d array as strategies are arrays themselves before converting to str
    agent_strategies = [[str([round(val, 2) for val in strategy]) for strategy in row] for row in agent_strategies]
    agent_strategies = pd.DataFrame(np.asarray(agent_strategies))

    # Now flatten out strategies to just be a string rather than the strategy array for processing
    # To data frames for easier file processing
    agent_decisions = pd.DataFrame(np.concatenate(agent_decisions))
    entrance_rates = pd.DataFrame(np.asarray(entrance_rates).T)

    filename = f"{args.c}-{args.lr}-{args.N}"

    entrance_rates.to_csv(args.output_folder + "attendance-" + filename + ".csv")
    agent_decisions.to_csv(args.output_folder + "decisions-" + filename + ".csv.gv", compression='gzip')
    agent_strategies.to_csv(args.output_folder + "strategies-" + filename + ".csv.gv", compression='gzip')


if __name__ == '__main__':
    args = arg_parser()
    main(args)

