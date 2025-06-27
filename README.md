# Agent-Based Market Simulator with LLM-Driven Behavior

This project simulates a simplified market where multiple trading agents interact by placing buy and sell orders. Each agent can follow predefined strategies or use a local language model to decide trading actions. The simulator is designed for experimenting with market dynamics, strategy benchmarking, and agent-based modeling.

---

## Features

- integration with a local language model
- Core market engine for matching and settling trades
- Logging of price evolution, trade history, and agent states
- Easily extendable for new strategies or agent types

---

## Requirements

- Python 3.9 or higher

Install dependencies:

```bash
pip install -r requirements.txt


python main.py --strategy random --traders 5 --ticks 50 --init-price 10


