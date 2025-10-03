# Edward Lloyd's Coffeehouse - Ship Insurance Simulation

A Pygame-based simulation of the early insurance industry, set in Edward Lloyd's coffeehouse in 18th century London.

## Overview

This game simulates ship insurance in the 1760s, where players act as underwriters in Edward Lloyd's famous coffeehouse. You'll negotiate premiums, assess risks, and compete with other insurers to build your business.

## Features

- **Historical Simulation**: Based on real 18th-century shipping and insurance practices
- **Risk Assessment**: Evaluate ships based on age, condition, routes, and weather
- **Premium Negotiation**: Set competitive premiums while managing risk
- **Dynamic Weather**: Ships face realistic hazards like storms, pirates, and icebergs
- **Economic Simulation**: Track revenue, claims, and profitability

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Project Structure

```
src/
├── core/           # Main game logic and entry point
├── models/         # Game objects (Ship, Insurer, Weather)
├── ui/             # User interface components
│   ├── menus/      # Menu screens
│   ├── screens/    # Game screens
│   └── components/ # Reusable UI components
├── data/           # Game data and configuration
├── utils/          # Utility functions and algorithms
└── assets/         # Images, sounds, and data files
```

## Gameplay

1. **Information Pages**: Learn about ships, ports, routes, and hazards
2. **Risk Preferences**: Set your underwriting criteria
3. **Premium Negotiation**: Compete with other insurers in the coffeehouse
4. **Ship Tracking**: Watch ships sail and face various perils
5. **Financial Management**: Track premiums, claims, and profits

## Development

This project follows modern Python packaging practices with a clean, modular structure that makes it easy to extend and maintain.

## Credits

Developed by Hughes Consultancy and Research Ltd.
Historical research based on Lloyd's Register of Shipping and maritime archives.
