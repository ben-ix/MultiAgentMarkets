import numpy as np
import pandas as pd
from utils import arg_parser
from src.market import Market


def main(args):
    entrance_rates = []
    agent_decisions = []
    agent_resources = []

    # Run multiples times to account for stochasticity
    n_runs = 30
    for _ in range(n_runs):
        market = Market(args.N, args.c, args.lr, args.M)
        market.run(args.T)
        individual_run = market.results()
        entrance_rates.append(individual_run["entrance_rates"])
        agent_decisions.append(individual_run["decisions"])
        agent_resources.append(individual_run["resources"])

    # To data frames for easier file processing
    entrance_rates = pd.DataFrame(np.asarray(entrance_rates).T)
    agent_decisions = pd.DataFrame(np.concatenate(agent_decisions))
    agent_resources = pd.DataFrame(np.concatenate(agent_resources))

    filename = f"{args.c}-{args.lr}-{args.N}"

    output_folder = args.output_folder
    entrance_rates.to_csv(output_folder + "attendance-" + filename + ".csv")
    agent_decisions.to_csv(output_folder + "decisions-" + filename + ".csv.gz", compression='gzip')
    agent_resources.to_csv(output_folder + "resources-" + filename + ".csv.gz", compression='gzip')


if __name__ == '__main__':
    args = arg_parser()
    main(args)

