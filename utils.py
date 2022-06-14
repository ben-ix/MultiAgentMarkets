import argparse


def arg_parser():
    parser = argparse.ArgumentParser()

    # Allow entering c (enjoyable capacity) as either a float (0..1), or an integer (0..100)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--c", type=float, help="Enjoyable capacity rate")
    group.add_argument("--cint", type=int, help="Enjoyable capacity rate (as integer 0..100),"
                                                "converted to float by dividing by 100")
    # Other parameters
    parser.add_argument("--lr", type=float, default=1, help="Learning Rate")
    parser.add_argument("--N", type=int, default=100, help="Number of Agents")
    parser.add_argument("--T", type=int, default=1000, help="Timesteps")
    parser.add_argument("--M", type=int, default=10, help="Memory Length")

    # Saving output
    parser.add_argument("--output_folder", type=str, default="results/", help="Where to save output")

    args = parser.parse_args()

    # When running from command line we can pass in integer to make array jobs easier
    if args.c is None:
        args.c = args.cint / 100

    print(args)

    return args
