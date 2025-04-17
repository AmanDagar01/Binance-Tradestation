# Binance Trading Bot

This project is a Python application that interacts with the Binance API to manage trading operations. It allows users to create and cancel orders, view existing orders and positions, and subscribe to ticker updates for a specified duration.

## Features

- Create orders
- Cancel orders
- View orders
- View positions
- Subscribe to ticker updates

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AmanDagar01/Binance-Tradestation.git
   cd binance-trading-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the prompts to interact with the Binance API.

## Configuration

Before running the application, ensure that you have set up your API keys in the `src/utils/config.py` file.

## Running Tests

To run the unit tests for the BinanceClient class, use:
```
pytest tests/test_client.py
```
