import sys
import argparse
from controllers.simulationController import SimulationController

def parse_args():
    parser = argparse.ArgumentParser("Market Simulator CLI")
    parser.add_argument(
        "--strategy",
        choices=["llm", "random", "rsi", "bollinger"],
        default="llm",
        help="Which trading strategy to run",
    )
    parser.add_argument(
        "--traders", type=int, default=5,
        help="Number of trader agents (default: 5)",
    )
    parser.add_argument(
        "--ticks", type=int, default=50,
        help="Simulation ticks (default: 50)",
    )
    parser.add_argument(
        "--init-price", type=float, default=100.0,
        help="Starting market price (default: 100.0)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    controller = SimulationController(
        num_traders=args.traders,
        ticks=args.ticks,
        init_price=args.init_price,
        strategy_name=args.strategy,
        seed=args.seed,
    )
    controller.run() #ignore
    return 0

if __name__ == "__main__":
    sys.exit(main())
