# Agent-Based Market Simulator with LLM-Driven Behavior

This project simulates a simplified market where multiple trading agents interact by placing buy and sell orders. Each agent can follow predefined strategies or use a local language model to decide trading actions. The simulator is designed for experimenting with market dynamics, strategy benchmarking, and agent-based modeling.

---

## Overview

The entry point of the project is main.py. It acts as a wrapper over the CLI defined in presenter/cli.py. 

The CLI parses arguments like strategy, number of traders, ticks, and initial price.

 This is a thin presentation layer that merely gathers input and instantiates the simulation controller. 

The CLI is not tightly coupled with business logic. This is aligned with the Clean Architecture idea of separating interface (CLI) from core logic.

---

## Dependency Injection (SimulationController)

The heart of the setup is the SimulationController 

Its constructor takes the CLI parameters and creates the needed components. For example, it instantiates TraderDb and MarketDb, then wraps them in TraderAccess and MarketAccess, and picks a strategy. 

Each dependency is passed through the constructor (a form of constructor injection), rather than being hard-coded internally.

This ensures low coupling and high flexibility. For instance, I can inject a different StrategyEngine (e.g., LLM-based vs Random) without changing controller logic.

Impact Point: “It follows the Dependency Inversion Principle, where high-level modules are not dependent on low-level implementations.”

Here we see that the controller builds and injects all necessary objects explicitly via __init__, which keeps classes loosely coupled. The controller then calls run(), which creates Trader entities and starts the market engine.

---

## Market Engine (Entities & Data Access)

The MarketEngine (in engines/market_engine.py) runs the simulation loop.
It accesses the current market state and traders through the resource-access layer:

In each tick, it queries the LLMEngine for each trader’s decision, updates each trader’s cash/inventory via Trader.try_buy/try_sell, and updates the market price via Market.update_price(net_demand).

 All state changes are written back to the in-memory databases through the TraderAccess and MarketAccess layers.

This separation means the market engine never manipulates raw data

It’s just the center of business use cases. Entities and interfaces are directly used here.

---

## Entities

Business Logic Encapsulation (Trader & Market Entities): All core trading logic is encapsulated inside the entity classes in entities/. For example, Trader has methods try_buy(volume, price) and try_sell(volume, price) which enforce cash/inventory constraints and update its own state. The Market entity has update_price(net_demand) which computes the next price based on demand. These classes bundle their data (cash, inventory, price_history, etc.) with methods to operate on that data. This is classic OOP encapsulation: implementation details (like how net worth is calculated or how price is adjusted) are hidden within the class. Importantly, these methods contain no external dependencies – they don’t call databases or I/O. This matches the clean architecture principle that the core domain (inner circle) is independent of infrastructure. In other words, our Trader and Market classes represent the “pure” business rules at the center of the design.


---

## Strategies

The simulation uses a Strategy Pattern for trading behavior. The file strategies/base.py defines a Strategy interface with sbastract method decide which every class which will inherit strategy class has to have

Concrete strategies (LLM, Random, RSI, Bollinger) inherit from this base and implement decide. This mirrors the strategy pattern: the context (here LLMEngine or more generally the simulation engine) uses a strategy interface and can swap out the concrete algorithm easilyrefactoring.gururefactoring.guru. For example, LLMStrategy uses an OpenAI model to decide actions, while RandomStrategy picks a random action. The simulation controller picks the strategy class by name, and wraps it with LLMEngine, which simply holds a strategy and calls strategy.decide()

Thus, adding a new strategy only requires creating a new class that implements decide, with no changes to the engine logic.

---

## Setup

- Requirements
```bash
pip install -r requirements.txt
```

- Run the project
```bash
python main.py --strategy random --traders 5 --ticks 50 --init-price 10
```


