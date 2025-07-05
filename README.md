# Agent-Based Market Simulator with LLM-Driven Behavior

This project simulates a simplified market where multiple trading agents interact by placing buy and sell orders. Each agent can follow predefined strategies or use a local language model to decide trading actions. The simulator is designed for experimenting with market dynamics, strategy benchmarking, and agent‑based modeling.

## Overview

The entry point of the project is `main.py`, which wraps the CLI defined in `presenter/cli.py`. The CLI parses arguments such as strategy, number of traders, ticks, and initial price. It simply gathers input and instantiates the simulation controller, keeping the interface separate from core logic in line with Clean Architecture principles.

## Dependency Injection (SimulationController)

The `SimulationController` constructor takes the CLI parameters and creates all necessary components. For example, it instantiates `TraderDb` and `MarketDb`, wraps them in `TraderAccess` and `MarketAccess`, and selects a strategy. By passing each dependency through the constructor rather than hard‑coding them, the design achieves low coupling and high flexibility: you can swap in a different `StrategyEngine` without changing controller code. This follows the Dependency Inversion Principle, ensuring high‑level modules do not depend on low‑level implementations.

## Market Engine (Entities & Data Access)

The `MarketEngine` in `engines/market_engine.py` runs the simulation loop. On each tick, it queries the `LLMEngine` for each trader’s decision, updates cash and inventory via `Trader.try_buy()` or `Trader.try_sell()`, and adjusts the market price with `Market.update_price(net_demand)`. All state changes are written back through the `TraderAccess` and `MarketAccess` layers, so the engine never manipulates raw data directly.


## LLM Strategy and Prompting

The `LLMStrategy` wraps an underlying strategy implementation and formulates a structured prompt for the language model at each tick. The prompt includes the current price, trader state (cash, inventory), and recent price history in JSON. The LLM returns a JSON object with a `quantity` field indicating how many units to buy (>0) or sell (<0). This approach keeps prompts self‑contained and machine‑parsable, minimizing ambiguity and simplifying error handling.


## Entities

All core trading logic is encapsulated in the entity classes under `entities/`. For example, `Trader` methods `try_buy(volume, price)` and `try_sell(volume, price)` enforce cash and inventory constraints, while `Market.update_price(net_demand)` computes the next price based on demand. These classes bundle data and behavior without external dependencies, aligning with the idea that the domain layer remains independent of infrastructure.

## Resource Access Layer and In‑Memory Databases

The resource access layer abstracts how traders and market data are stored and retrieved. We use simple in‑memory databases (`TraderDb` and `MarketDb`) behind access objects (`TraderAccess`, `MarketAccess`) that expose only the methods the engine needs (e.g., `get_all_traders()`, `save_trader()`). This keeps the market engine and controller unaware of storage details, making it easy to swap in a persistent database later without touching business logic.


## Strategies

The simulation uses a Strategy Pattern for trading behavior. The file `strategies/base.py` defines a `Strategy` interface with an abstract `decide()` method. Concrete strategies such as LLM, Random, RSI, or Bollinger inherit from this base and implement `decide()`. The controller selects the strategy by name and invokes `strategy.decide()` through the `LLMEngine`. Adding a new strategy only requires creating a class that implements `decide()`, with no changes needed elsewhere.

## Setup

- **Install dependencies**  
  ```bash
  pip install -r requirements.txt
  ```

- Run the project
  ```bash
  python main.py --strategy random --traders 5 --ticks 50 --init-price 10
  ```


